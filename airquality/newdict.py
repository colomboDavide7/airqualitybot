######################################################
#
# Author: Davide Colombo
# Date: 24/12/21 17:13
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict
from datetime import datetime
from collections import namedtuple
from airquality.urlfmt import URLFormatter
from airquality.sqldict import FrozenSQLDict
from airquality.sqltable import JoinSQLTable, SQLTable
from airquality.dbadapter import DBAdapterABC
from airquality.iterableurl import IterableURL, AtmotubeIterableURL


class APIParamLookup(namedtuple('APIParamLookup', ['pkey', 'record'])):

    @property
    def sensor_id(self) -> int:
        return self.record[0]

    @property
    def api_key(self) -> str:
        return self.record[1]

    @property
    def api_id(self) -> str:
        return self.record[2]

    @property
    def ch_name(self) -> str:
        return self.record[3]

    @property
    def last_activity(self) -> datetime:
        return self.record[4]

    @last_activity.setter
    def last_activity(self, value: datetime):
        self.record[4] = value

    @property
    def private_url_options(self) -> Dict[str, str]:
        return {'api_key': self.api_key, 'api_id': self.api_id}

    @property
    def sql_record(self):
        return f"{self.sensor_id}, '{self.api_key}', '{self.api_id}', '{self.ch_name}', '{self.last_activity}'"

    def __repr__(self):
        return f"{type(self).__name__}(pkey={self.pkey}, record={self.record!r})"


class MeasureDict(FrozenSQLDict):
    
    def __init__(self, apiparam_table: JoinSQLTable, dbadapter: DBAdapterABC, measure_table: SQLTable, url_formatter: URLFormatter):
        super(MeasureDict, self).__init__(table=apiparam_table, dbadapter=dbadapter)
        self.measure_table = measure_table
        self.url_formatter = url_formatter

    @property
    def sensor_api_param(self):
        return (APIParamLookup(pkey=pkey, record=record) for pkey, record in self.items())

    @property
    def all_urls(self):
        return (self.url_formatter.format_url(**param.private_url_options) for param in self.sensor_api_param)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for p in self.sensor_api_param:
            print(repr(p))
        print('\n\n\n')
        for url in self.all_urls:
            print(url)

        # TODO: push all the values
        # TODO: flush the memory buffer

    def __repr__(self):
        return f"{type(self).__name__}(apiparam_table={self.table}, dbadapter={self.dbadapter}, " \
               f"measure_table={self.measure_table}, url_formatter={self.url_formatter!r})"


# class AtmotubeMeasureDict(MeasureDict):
#
#     def __init__(self, url_factory=AtmotubeIterableURL):
#         self.url_factory = url_factory
#
#     def all_urls(self):
#         if not self._all_urls:
#             for pkey, record in self.items():
#                 _, api_key, api_id, ch_name, last_activity = record
#                 url = url_template.format(api_key=api_key, api_id=api_id, api_fmt="json")
#                 self._all_urls.add(IterableURL(url_template=url, begin=last_activity))
#         return self._all_urls
