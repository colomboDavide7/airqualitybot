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
from airquality.sqldict import SelectOnlyWhereDict, SelectInsertDict, UpdateDict, JoinFilterDict


def atmotube():
    # TODO: read from environment
    connection_string = "dbname=airquality host=localhost port=5432 user=root password=a1R-d3B-R00t!"

    apiparam_update = UpdateDict(table="api_param", pkey="id", dbconn=connection_string, selected_cols=APIPARAM_COLS)
    mobile_measure_table = SelectInsertDict(dbconn=connection_string, table="mobile_measurement", pkey="id", selected_cols=MOBILE_MEASURE_COLS)
    measure_param_table = SelectOnlyWhereDict(dbconn=connection_string, table="measure_param", pkey="id",
                                              selected_cols=MEASUREPARAM_COLS, filter_attr="param_name", filter_value="atmotube")
    sensor_apiparam_join = JoinFilterDict(conn=connection_string, join_table="sensor", join_key="id",
                                          table="api_param", pkey="sensor_id", cols_of_interest=APIPARAM_COLS,
                                          join_filter_col="sensor_type", join_filter_val="atmotube")

    param_code_id = {}
    for key, value in measure_param_table.items():
        code, name, unit = value
        print(f"found param with id={key}, code={code}, name={name}, unit={unit}")
        param_code_id[code] = key

    counter = count(mobile_measure_table.max_id())
    for key, value in sensor_apiparam_join.items():
        sensor_id, api_key, api_id, ch_name, last_activity = value
        print(f"found Atmotube sensor with id={sensor_id}, api_key={api_key}, api_id={api_id}, ch_name={ch_name}, active at {last_activity}")

        url = atmotube_url.format(api_key=api_key, api_id=api_id) + "&date={date}"

        now = datetime.now()
        begin = last_activity + timedelta(0)
        print(f"start to look for new measurements at: {begin!s}")
        while begin <= now:
            date_to_lookat = extract_date(timestamp=begin, fmt=ATMOTUBE_DATE_FORMAT)
            url_with_date = url.format(date=date_to_lookat)
            responses = AtmotubeResponses(url=url_with_date, items_of_interest=ITEMS_OF_INTEREST, filter_ts=last_activity)
            for resp in responses:
                print(f"found new response at {resp.measured_at}: values={resp.values!r}, coords={resp.coords}")
                for code, val in resp.values:
                    record_id = next(counter)
                    param_id = param_code_id[code]
                    mobile_measure_table[record_id] = f"{param_id}, {wrap_value(val)}, '{resp.measured_at}', {resp.coords}"

            if responses:
                # commit all the measurements at once
                print("insert")
                mobile_measure_table.insert()

                # Update last activity field at the acquisition time of the last measure stored
                print("update last acquisition")
                last_acquisition = responses[-1].measured_at
                print(last_acquisition)
                apiparam_update[key] = f"{sensor_id}, '{api_key}', '{api_id}', '{ch_name}', '{last_acquisition}'"

            begin = add_days(begin, days=1)


def wrap_value(value: str, default="NULL") -> str:
    return f"'{value}'" if value is not None else default


ATMOTUBE_DATE_FORMAT = "%Y-%m-%d"


def extract_date(timestamp: datetime, fmt=ATMOTUBE_DATE_FORMAT) -> str:
    return timestamp.date().strftime(fmt)


def add_days(timestamp: datetime, days: int) -> datetime:
    return timestamp + timedelta(days=days)
