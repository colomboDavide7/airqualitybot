######################################################
#
# Author: Davide Colombo
# Date: 18/12/21 18:10
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
# TODO: load from the environment file
atmotube_url = "https://api.atmotube.com/api/v1/data?api_key={api_key}&mac={api_id}&order=asc&format=json"

MOBILE_MEASURE_COLS = ['param_id', 'param_value', 'timestamp', 'geom']
ITEMS_OF_INTEREST = ['time', 'voc', 'pm1', 'pm25', 'pm10', 't', 'h', 'p', 'coords']
ATMOTUBE_PARAM_NAMES = {'voc', 'pm1', 'pm25', 'pm10', 't', 'h', 'p'}
SENSOR_COLS = ['sensor_type', 'sensor_name']
APIPARAM_COLS = ['sensor_id', 'ch_key', 'ch_id', 'ch_name', 'last_acquisition']
GEOLOCATION_COLS = ['sensor_id', 'valid_from', 'geom']
MEASUREPARAM_COLS = ['param_code', 'param_name', 'param_unit']
SQL_DATETIME_FMT = "%Y-%m-%d %H:%M:%S"
ST_GEOM = "ST_GeomFromText('{geom}', {srid})"
POSTGIS_POINT = "POINT({lon} {lat})"

from typing import Dict, Any
from datetime import datetime, timedelta


class AtmotubeItem(object):
    ATMOTUBE_MEASURE_PARAM = ['voc', 'pm1', 'pm25', 'pm10', 't', 'h', 'p']

    def __init__(self, item: Dict[str, Any]):
        self.item = item
        self._at = None
        self._coords = None
        self._at_datetime = None

    def __gt__(self, other):
        if not isinstance(other, datetime):
            raise TypeError(f"{type(self).__name__} expected 'datetime' object, got {type(other).__name__}")
        return (self.measured_at_datetime - other).total_seconds() > 0

    @property
    def measured_at_datetime(self) -> datetime:
        if self._at_datetime is None:
            self._at_datetime = datetime.strptime(self.measured_at, SQL_DATETIME_FMT)
        return self._at_datetime

    @property
    def measured_at(self) -> str:
        if self._at is None:
            self._at = self.item['time'].replace("T", " ").split('.')[0]
        return self._at

    @property
    def coords(self):
        if self._coords is None:
            tmp = self.item.pop('coords', None)
            self._coords = "NULL"
            if tmp is not None:
                pt = POSTGIS_POINT.format(lat=tmp['lat'], lon=tmp['lon'])
                self._coords = ST_GEOM.format(geom=pt, srid=26918)
        return self._coords

    @property
    def values(self):
        return [(pcode, self.item.get(pcode)) for pcode in self.ATMOTUBE_MEASURE_PARAM]


from typing import Generator, List
from collections.abc import Iterable
from urllib.request import urlopen
from json import loads


class AtmotubeResponses(Iterable):

    def __init__(self, url: str, items_of_interest: List[str], filter_ts: datetime, default=None):
        self.items_of_interest = items_of_interest
        self.default = default
        self.filter_ts = filter_ts
        self.url = url
        with urlopen(self.url) as resp:
            self.parsed = loads(resp.read())

    def __getitem__(self, index) -> AtmotubeItem:
        if index >= len(self):
            raise IndexError(f"{type(self).__name__} index {index} out of range")
        return AtmotubeItem(self.parsed['data']['items'][index])

    def __iter__(self) -> Generator[AtmotubeItem, None, None]:
        items = (AtmotubeItem(item) for item in self.parsed['data']['items'])
        for item in items:
            if item > self.filter_ts:
                yield item

    def __len__(self):
        items = (AtmotubeItem(item) for item in self.parsed['data']['items'])
        return sum(1 for item in items if item.measured_at_datetime > self.filter_ts)


from itertools import count
from airquality.sqltable import FilterSQLTable, JoinSQLTable, SQLTable
from airquality.sqldict import FrozenSQLDict, MutableSQLDict, HeavyweightMutableSQLDict


def atmotube():
    # TODO: read from environment
    connection_string = "dbname=airquality host=localhost port=5432 user=root password=a1R-d3B-R00t!"

    mobile_measure_table = SQLTable(dbconn=connection_string, table_name="mobile_measurement", pkey="id", selected_cols=MOBILE_MEASURE_COLS)
    frozen_mobile_dict = FrozenSQLDict(table=mobile_measure_table)
    heavyweight_mobile_dict = HeavyweightMutableSQLDict(sqldict=frozen_mobile_dict)

    atmotube_measure_param_table = FilterSQLTable(
            dbconn=connection_string,
            table_name="measure_param",
            pkey="id",
            selected_cols=MEASUREPARAM_COLS,
            filter_col="param_name",
            filter_val="atmotube"
    )

    frozen_measure_param_dict = FrozenSQLDict(table=atmotube_measure_param_table)

    atmotube_sensor_table = FilterSQLTable(
        dbconn=connection_string,
        table_name="sensor",
        pkey="id",
        selected_cols=SENSOR_COLS,
        filter_col="sensor_type",
        filter_val="atmotube",
        alias="s")

    atmotube_apiparam_table = JoinSQLTable(
            dbconn=connection_string,
            table_name="api_param",
            pkey="id",
            fkey="sensor_id",
            selected_cols=APIPARAM_COLS,
            alias="a",
            join_table=atmotube_sensor_table
    )

    frozen_apiparam_dict = FrozenSQLDict(table=atmotube_apiparam_table)
    mutable_apiparam_dict = MutableSQLDict(sqldict=frozen_apiparam_dict)

    param_code_id = {}
    for key, value in frozen_measure_param_dict.items():
        code, name, unit = value
        print(f"found param with id={key}, code={code}, name={name}, unit={unit}")
        param_code_id[code] = key

    counter = count(heavyweight_mobile_dict.start_id)
    for pkey, record in mutable_apiparam_dict.items():
        sensor_id, api_key, api_id, ch_name, last_activity = record
        print(f"found Atmotube sensor with id={sensor_id}: {record!r}")

        url = atmotube_url.format(api_key=api_key, api_id=api_id) + "&date={date}"

        now = datetime.now()
        begin = last_activity + timedelta(0)
        while begin <= now:
            date_to_lookat = extract_date(timestamp=begin, fmt=ATMOTUBE_DATE_FORMAT)
            url_with_date = url.format(date=date_to_lookat)
            responses = AtmotubeResponses(url=url_with_date, items_of_interest=ITEMS_OF_INTEREST, filter_ts=last_activity)
            for resp in responses:
                print(f"found new response at {resp.measured_at}: values={resp.values!r}, coords={resp.coords}")
                for code, val in resp.values:
                    record_id = next(counter)
                    param_id = param_code_id[code]
                    heavyweight_mobile_dict[record_id] = f"{param_id}, {wrap_value(val)}, '{resp.measured_at}', {resp.coords}"

            if responses:
                # commit all the measurements at once
                heavyweight_mobile_dict.commit()

                # Update last activity field at the acquisition time of the last measure stored
                last_acquisition = responses[-1].measured_at
                mutable_apiparam_dict[pkey] = f"{sensor_id}, '{api_key}', '{api_id}', '{ch_name}', '{last_acquisition}'"

            begin = add_days(begin, days=1)


def wrap_value(value: str, default="NULL") -> str:
    return f"'{value}'" if value is not None else default


ATMOTUBE_DATE_FORMAT = "%Y-%m-%d"


def extract_date(timestamp: datetime, fmt=ATMOTUBE_DATE_FORMAT) -> str:
    return timestamp.date().strftime(fmt)


def add_days(timestamp: datetime, days: int) -> datetime:
    return timestamp + timedelta(days=days)
