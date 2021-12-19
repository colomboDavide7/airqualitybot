######################################################
#
# Author: Davide Colombo
# Date: 19/12/21 11:39
# Description: INSERT HERE THE DESCRIPTION
#
######################################################

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

from typing import Dict, Any, Generator, List, Set
from collections.abc import Iterable
from collections import namedtuple
from urllib.request import urlopen
from json import loads


class ChannelProperties(namedtuple('ChannelProperties', ['key', 'ident', 'name'])):

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name}, key=XXX, ident=XXX)"


class PurpleairItem(object):

    CHANNELS_PARAM = [{'key': 'primary_key_a', 'ident': 'primary_id_a', 'name': '1A'},
                      {'key': 'primary_key_b', 'ident': 'primary_id_b', 'name': '1B'},
                      {'key': 'secondary_key_a', 'ident': 'secondary_id_a', 'name': '2A'},
                      {'key': 'secondary_key_b', 'ident': 'secondary_id_b', 'name': '2B'}]

    def __init__(self, item: Dict[str, Any]):
        self.item = item
        self._channels = []
        self._geom = ""
        self._name = ""
        self._at = ""

    @property
    def name(self) -> str:
        if not self._name:
            self._name = f"{self.item['name']} ({self.item['sensor_index']})"
        return self._name

    @property
    def type(self) -> str:
        return "Purpleair/Thingspeak"

    @property
    def located_at(self) -> str:
        if not self._geom:
            point = POSTGIS_POINT.format(lon=self.item['longitude'], lat=self.item['latitude'])
            self._geom = ST_GEOM.format(geom=point, srid=26918)
        return self._geom

    @property
    def created_at(self) -> str:
        if not self._at:
            self._at = datetime.fromtimestamp(self.item['date_created']).strftime(SQL_DATETIME_FMT)
        return self._at

    @property
    def channel_properties(self) -> Set[ChannelProperties]:
        if not self._channels:
            self._channels = {ChannelProperties(key=self.item[p['key']], ident=self.item[p['ident']], name=p['name'])
                              for p in self.CHANNELS_PARAM}
        return self._channels

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name}, created_at={self.created_at}, located_at={self.located_at}, " \
               f"channels={self.channel_properties!r})"


class PurpleairResponses(Iterable):

    def __init__(self, url: str, existing_names: List[str]):
        self.existing_names = existing_names
        with urlopen(url) as resp:
            resp = loads(resp.read())
            self.fields = resp['fields']
            self.data = resp['data']

    def __iter__(self) -> Generator[PurpleairItem, None, None]:
        items = (PurpleairItem(dict(zip(self.fields, d))) for d in self.data)
        for item in items:
            if item.name not in self.existing_names:
                yield item

    def __len__(self):
        items = (PurpleairItem(dict(zip(self.fields, d))) for d in self.data)
        return sum(1 for item in items if item.name not in self.existing_names)


from itertools import count
from datetime import datetime
from airquality.sqltable import SQLTable, FilterSQLTable
from airquality.sqldict import MutableSQLDict, FrozenSQLDict


def purpleair():

    connection_string = "dbname=airquality host=localhost port=5432 user=root password=a1R-d3B-R00t!"

    sensor_table = FilterSQLTable(
        dbconn=connection_string,
        table_name="sensor", pkey="id",
        selected_cols=SENSOR_COLS,
        filter_col="sensor_type",
        filter_val="purpleair"
    )
    frozen_sensor_dict = FrozenSQLDict(table=sensor_table)
    mutable_sensor_dict = MutableSQLDict(sqldict=frozen_sensor_dict)

    apiparam_table = SQLTable(dbconn=connection_string, table_name="api_param", pkey="id", selected_cols=APIPARAM_COLS)
    frozen_apiparam_dict = FrozenSQLDict(table=apiparam_table)
    mutable_apiparam_dict = MutableSQLDict(sqldict=frozen_apiparam_dict)

    geolocation_table = SQLTable(dbconn=connection_string, table_name="sensor_at_location", pkey="id", selected_cols=GEOLOCATION_COLS)
    frozen_geolocation_dict = FrozenSQLDict(table=geolocation_table)
    mutable_geolocation_dict = MutableSQLDict(sqldict=frozen_geolocation_dict)

    sensor_counter = count(mutable_sensor_dict.start_id)
    apiparam_counter = count(mutable_apiparam_dict.start_id)
    geolocation_counter = count(mutable_geolocation_dict.start_id)

    existing_names = []
    for pkey, record in mutable_sensor_dict.items():
        print(f"found sensor indexed by {pkey}: {record!r}")
        existing_names.append(record[1])

    responses = PurpleairResponses(url=purpleair_url, existing_names=existing_names)
    for resp in responses:
        print(f"found new response: {resp!r}")

        sensor_id = next(sensor_counter)
        mutable_sensor_dict[sensor_id] = f"'{resp.type}', '{resp.name}'"

        for chp in resp.channel_properties:
            mutable_apiparam_dict[next(apiparam_counter)] = \
                f"{sensor_id}, '{chp.key}', '{chp.ident}', '{chp.name}', '{resp.created_at}'"

        now = datetime.now().strftime(SQL_DATETIME_FMT)
        mutable_geolocation_dict[next(geolocation_counter)] = f"{sensor_id}, '{now}', NULL, {resp.located_at}"
