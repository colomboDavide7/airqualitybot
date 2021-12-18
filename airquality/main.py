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
MEASUREPARAM_COLS = ['param_code', 'param_name', 'param_unit']
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
        self._new_items = ""

    def insert(self):
        """Insert multiple elements """
        if not self._new_items:
            raise ValueError(f"{type(self).__name__} cannot insert '{self._new_items}' values")
        with self.conn.cursor() as cur:
            cur.execute(f"INSERT INTO {self.schema}.{self.table} VALUES {self._new_items.strip(',')};")
            self.conn.commit()
            self._new_items = ""

    def __setitem__(self, key, value):
        """Append values to '_new_items' in order to commit MANY changes into database at a time"""
        self._new_items += f"({key}, {value}),"

    def __getitem__(self, key):
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT {self.cols_of_interest()} FROM {self.schema}.{self.table} WHERE {self.pkey}={key}")
            self.conn.commit()
            row = cur.fetchone()
            if row is None:
                raise KeyError(f"{type(self).__name__} on '{self.table}' table => '__getitem__({key})'")
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
        return f"{type(self).__name__}(table={self.table}, conn={self.conn!r}, pkey={self.pkey}, " \
               f"cols_of_interest={self.cols_of_interest()}, schema={self.schema})"

    def max_id(self) -> int:
        if self._max_id is None:
            with self.conn.cursor() as cur:
                cur.execute(f"SELECT MAX({self.pkey}) FROM {self.schema}.{self.table};")
                self.conn.commit()
                x_id = cur.fetchone()[0]
                self._max_id = 1 if x_id is None else x_id + 1
        return self._max_id

    def cols_of_interest(self) -> str:
        if self._cols_of_interest_str is None:
            self._cols_of_interest_str = ','.join(f"{item}" for item in self._cols_of_interest)
        return self._cols_of_interest_str

    def close(self):
        self.conn.close()


from airquality.atmotube import atmotube


def main():
    args = sys.argv[1:]
    if len(args) != 1:
        print("USAGE => python(version) -m airquality [purpleair|atmotube]")
        sys.exit(1)

    personality = args[0]
    print(personality)
    start = perf_counter()
    try:
        if personality == 'purpleair':
            purpleair()
        elif personality == 'atmotube':
            atmotube()
        else:
            raise ValueError(f"Wrong command line argument '{personality}'")
    except (HTTPError, ValueError, KeyError, psycopg2.errors.Error) as err:
        print(f"{err!r} exception caught in {main.__name__}")
        sys.exit(1)

    stop = perf_counter()
    print(f"success in {stop - start} seconds")


def purpleair():
    purpleair_responses = PurpleairResponses(url=purpleair_url)
    connection_string = "dbname=airquality host=localhost port=5432 user=root password=a1R-d3B-R00t!"

    sensor_table = SQLDict(table="sensor", pkey="id", conn=connection_string, cols_of_interest=SENSOR_COLS)
    apiparam_table = SQLDict(table="api_param", pkey="id", conn=connection_string, cols_of_interest=APIPARAM_COLS)
    geolocation_table = SQLDict(table="sensor_at_location", pkey="id", conn=connection_string,
                                cols_of_interest=GEOLOCATION_COLS)

    print(repr(sensor_table))
    print(repr(apiparam_table))
    print(repr(geolocation_table))

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

    purpleair_names = []
    for sensor_id, value in sensor_table.items():
        tp, fn = value
        if 'purpleair' in tp.lower():
            purpleair_names.append(fn)

    for resp in purpleair_responses:
        sensor_id = next(counter)
        fn = f"{resp['name']} ({resp['sensor_index']})"
        if fn not in purpleair_names:
            print(f"INSERTING {fn}")
            sensor_table[sensor_id] = f"'PurpleairThingspeak', '{fn}'"

            la = datetime.fromtimestamp(resp['date_created']).strftime(SQL_DATETIME_FMT)

            apiparam_id = next(apiparam_counter)
            apiparam_table[
                apiparam_id] = f"{sensor_id}, '{resp['primary_key_a']}', '{resp['primary_id_a']}', '1A', '{la}'"

            apiparam_id = next(apiparam_counter)
            apiparam_table[
                apiparam_id] = f"{sensor_id}, '{resp['primary_key_b']}', '{resp['primary_id_b']}', '1B', '{la}'"

            apiparam_id = next(apiparam_counter)
            apiparam_table[
                apiparam_id] = f"{sensor_id}, '{resp['secondary_key_a']}', '{resp['secondary_id_a']}', '2A', '{la}'"

            apiparam_id = next(apiparam_counter)
            apiparam_table[
                apiparam_id] = f"{sensor_id}, '{resp['secondary_key_b']}', '{resp['secondary_id_b']}', '2B', '{la}'"

            geolocation_id = next(geolocation_counter)
            now = datetime.now().strftime(SQL_DATETIME_FMT)
            point = POSTGIS_POINT.format(lon=resp['longitude'], lat=resp['latitude'])
            geom = ST_GEOM.format(geom=point, srid=26918)
            geolocation_table[geolocation_id] = f"{sensor_id}, '{now}', NULL, {geom}"
