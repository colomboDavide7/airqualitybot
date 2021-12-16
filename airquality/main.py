######################################################
#
# Author: Davide Colombo
# Date: 16/12/21 09:35
# Description: Restart from scratch
#
######################################################
import collections.abc
import itertools
import json
import sys
import psycopg2
from psycopg2.errors import Error
from urllib.request import urlopen
from urllib.error import HTTPError
from time import perf_counter
from datetime import datetime
from operator import itemgetter
from typing import List

purpleair_url = "https://api.purpleair.com/v1/sensors?" \
      "api_key=A57E57A3-D2B1-11EB-913E-42010A800082" \
      "&fields=name,latitude,longitude,altitude,date_created,secondary_id_b," \
      "secondary_key_b,secondary_id_a,secondary_key_a,primary_id_a," \
      "primary_key_a,primary_id_b,primary_key_b" \
      "&nwlng=9.133101&nwlat=45.211471&selng=9.190360&selat=45.173243"

bad_url = "https://api.purpleair.com/v1/sensors?some_bad_field=some_value"


SENSOR_COLS = ['sensor_type', 'sensor_name']
APIPARAM_COLS = ['sensor_id', 'ch_key', 'ch_id', 'ch_name', 'last_acquisition']
GEOLOCATION_COLS = ['sensor_id', 'valid_from', 'geom']
SQL_DATETIME_FMT = "%Y-%m-%d %H:%M:%S"
ST_GEOM = "ST_GeomFromText('{geom}', {srid})"
POSTGIS_POINT = "POINT({lon} {lat})"


class PurpleairResponses(object):

    def __init__(self, url: str):
        with urlopen(url) as resp:
            print(f"response length={resp.length} bytes")
            print(f"response code={resp.code}")
            print(f"response msg={resp.msg}")
            self.resp = json.loads(resp.read())
        field = self.resp['fields']
        data = self.resp['data']
        self.items = (dict(zip(field, d)) for d in data)

    def __iter__(self):
        for item in self.items:
            yield item


class SQLDict(collections.abc.MutableMapping):

    def __init__(self, table: str, conn: str, pkey: str, cols_of_interest: List[str], schema="level0_raw"):
        self.conn = psycopg2.connect(conn)
        self.table = table
        self.schema = schema
        self.pkey = pkey
        self._cols_of_interest = cols_of_interest
        self._cols_of_interest_str = None
        self._max_id = None

    def __setitem__(self, key, value):
        """Insert a record composed as (id, type, name) into the sensor table. Ids of a new record starts at '_max_id'."""
        if key in self:
            return
        with self.conn.cursor() as cur:
            cur.execute(f"INSERT INTO {self.schema}.{self.table} VALUES ({key}, {value})")
            self.conn.commit()

    def __getitem__(self, key):
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT {self.cols_of_interest()} FROM {self.schema}.{self.table} WHERE {self.pkey}={key}")
            self.conn.commit()
            row = cur.fetchone()
            if row is None:
                raise KeyError(f"{self.__class__.__name__} on '{self.table}' table cannot found {self.pkey}='{key}' in "
                               f"'{self.__getitem__.__name__}' method")
            return row

    def __delitem__(self, key):
        """The DELETE operation is not supported"""
        pass

    def __len__(self) -> int:
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT COUNT(*) FROM {self.schema}.{self.table};")
            self.conn.commit()
            return cur.fetchone()[0]

    def __iter__(self):
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT {self.pkey} FROM {self.schema}.{self.table};")
            self.conn.commit()
            return map(itemgetter(0), cur.fetchall())

    def __repr__(self):
        return f"{type(self).__name__}(table={self.table}, schema={self.schema}, conn={self.conn!r}, pkey={self.pkey}, " \
               f"cols_of_interest={self.cols_of_interest()})"

    def max_id(self) -> int:
        if self._max_id is None:
            with self.conn.cursor() as cur:
                cur.execute(f"SELECT MAX({self.pkey}) FROM {self.schema}.{self.table};")
                self.conn.commit()
                x_id = cur.fetchone()[0]
                self._max_id = 1 if x_id is None else x_id+1
        return self._max_id

    def cols_of_interest(self) -> str:
        if self._cols_of_interest_str is None:
            self._cols_of_interest_str = ','.join(f"{item}" for item in self._cols_of_interest)
        return self._cols_of_interest_str

    def close(self):
        self.conn.close()


def main():
    start = perf_counter()
    try:
        purpleair_api_dict = PurpleairResponses(url=purpleair_url)
        connection_string = "dbname=airquality host=localhost port=5432 user=root password=a1R-d3B-R00t!"

        sensor_table = SQLDict(table="sensor", pkey="id", conn=connection_string, cols_of_interest=SENSOR_COLS)
        apiparam_table = SQLDict(table="api_param", pkey="id", conn=connection_string, cols_of_interest=APIPARAM_COLS)
        geolocation_table = SQLDict(table="sensor_at_location", pkey="id", conn=connection_string, cols_of_interest=GEOLOCATION_COLS)

        print(f"found #{len(sensor_table)} sensors")
        print(f"found #{len(apiparam_table)} api_parameters")
        print(f"found #{len(geolocation_table)} geolocations")

        # print(repr(sensor_table))
        # print(repr(apiparam_table))
        # print(repr(geolocation_table))

        # for key, value in sensor_table.items():
        #     tp, fn = value
        #     print(f"found sensor {fn} of type {tp} identified by {key}")

        # for key, value in apiparam_table.items():
        #     sensor_id, api_key, api_id, ch_name, last_activity = value
        #     print(f"found parameters for sensor {sensor_id}: key={api_key}, ident={api_id}, name={ch_name}, active={last_activity}")

        # for key, value in geolocation_table.items():
        #     valid_from, geom = value
        #     print(f"found sensor {key} at location {geom} valid from {valid_from}")

        counter = itertools.count(sensor_table.max_id())
        apiparam_counter = itertools.count(apiparam_table.max_id())
        geolocation_counter = itertools.count(geolocation_table.max_id())

        for item in iter(purpleair_api_dict):
            sensor_id = next(counter)
            fn = f"{item['name']} ({item['sensor_index']})"
            sensor_table[sensor_id] = f"'PurpleairThingspeak', '{fn}'"

            la = datetime.fromtimestamp(item['date_created']).strftime(SQL_DATETIME_FMT)

            apiparam_id = next(apiparam_counter)
            apiparam_table[apiparam_id] = f"{sensor_id}, '{item['primary_key_a']}', '{item['primary_id_a']}', '1A', '{la}'"

            apiparam_id = next(apiparam_counter)
            apiparam_table[apiparam_id] = f"{sensor_id}, '{item['primary_key_b']}', '{item['primary_id_b']}', '1B', '{la}'"

            apiparam_id = next(apiparam_counter)
            apiparam_table[apiparam_id] = f"{sensor_id}, '{item['secondary_key_a']}', '{item['secondary_id_a']}', '2A', '{la}'"

            apiparam_id = next(apiparam_counter)
            apiparam_table[apiparam_id] = f"{sensor_id}, '{item['secondary_key_b']}', '{item['secondary_id_b']}', '2B', '{la}'"

            geolocation_id = next(geolocation_counter)
            now = datetime.now().strftime(SQL_DATETIME_FMT)
            point = POSTGIS_POINT.format(lon=item['longitude'], lat=item['latitude'])
            geom = ST_GEOM.format(geom=point, srid=26918)
            geolocation_table[geolocation_id] = f"{sensor_id}, '{now}', NULL, {geom}"

    except (HTTPError, ValueError, KeyError, psycopg2.errors.Error) as err:
        print(f"{err!r} exception caught in {main.__name__}")
        sys.exit(1)

    stop = perf_counter()
    print(f"success in {stop-start} seconds")


# sensor_query.add(f"({sensor_id}, 'Purpleair/Thingspeak', '{fn}')")

# la = datetime.fromtimestamp(item['date_created']).strftime(SQL_DATETIME_FMT)
# apiparam_query.add(f"({sensor_id}, '{item['primary_key_a']}', '{item['primary_id_a']}', '1A', '{la}')")
# apiparam_query.add(f"({sensor_id}, '{item['primary_key_b']}', '{item['primary_id_b']}', '1B', '{la}')")
# apiparam_query.add(f"({sensor_id}, '{item['secondary_key_a']}', '{item['secondary_id_a']}', '2A', '{la}')")
# apiparam_query.add(f"({sensor_id}, '{item['secondary_key_b']}', '{item['secondary_id_b']}', '2B', '{la}')")

# now = datetime.now().strftime(SQL_DATETIME_FMT)
# point = POSTGIS_POINT.format(lon=item['longitude'], lat=item['latitude'])
# geom = ST_GEOM.format(geom=point, srid=26918)
# geolocation_query.add(f"({sensor_id}, '{now}', {geom})")

# with conn.cursor() as cur:
#     cur.execute(str(sensor_query))
#     cur.execute(str(apiparam_query))
#     cur.execute(str(geolocation_query))
#     conn.commit()

# print(sensor_query)
# print('\n')
# print(apiparam_query)
# print('\n')
# print(geolocation_query)




# class Number(object):
#
#     def __init__(self, minval=None, maxval=None):
#         self.minval = minval
#         self.maxval = maxval
#
#     def __set_name__(self, owner, name):
#         self.private_name = f'_{name}'
#
#     def __get__(self, instance, owner):
#         return getattr(instance, self.private_name)
#
#     def __set__(self, instance, value):
#         self.validate(value)
#         setattr(instance, self.private_name, value)
#
#     def validate(self, value):
#         if not isinstance(value, int):
#             raise TypeError(f"Expected {value!r} to be and int")
#         if self.minval is not None and value < self.minval:
#             raise ValueError(f"Expected {value!r} to be at least {self.minval}")
#         if self.maxval is not None and value > self.maxval:
#             raise ValueError(f"Expected {value!r} to be at most {self.maxval}")

# class SensorValue(object):
#
#     def __init__(self, ident: int, fn: str, tp: str):
#         self.ident = ident
#         self.fn = fn
#         self.tp = tp
#
#     def __str__(self):
#         return f"({self.ident}, '{self.tp}', '{self.fn}')"
#
#
# class APIParamValue(object):
#
#     def __init__(self, ident: int, api_key: str, api_id: str, api_fn: str,
#                  last_acquisition: datetime):
#         self.ident = ident
#         self.api_key = api_key
#         self.api_id = api_id
#         self.api_fn = api_fn
#         self.last_acquisition = last_acquisition
#
#     def __str__(self):
#         sql_timestamp = self.last_acquisition.strftime('%Y-%m-%d %H:%M:%S')
#         return f"({self.ident}, '{self.api_key}', '{self.api_id}', '{self.api_fn}', '{sql_timestamp}')"



# class InsertQuery(object):
#
#     def __init__(self, table: str, cols: List[str], schema="level0_raw"):
#         self.values = set()
#         self.cols = cols
#         self.header = f"INSERT INTO {schema}.{table} (" + ','.join(
#             f"{v}" for v in cols) + ") VALUES "
#
#     def add(self, value):
#         if not isinstance(value, str):
#             raise TypeError(f"{self.__class__.__name__} got {type(value)} required str or SensorValue")
#         self.values.add(value)
#
#     def __str__(self):
#         return self.header + ','.join(f"{v}" for v in self.values) + ';'


# sensor_query = InsertQuery(table="sensor", cols=SENSOR_COLS)
        # apiparam_query = InsertQuery(table="api_param", cols=APIPARAM_COLS)
        # geolocation_query = InsertQuery(table="sensor_at_location", cols=GEOLOCATION_COLS)
