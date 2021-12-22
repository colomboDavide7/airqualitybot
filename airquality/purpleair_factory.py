######################################################
#
# Author: Davide Colombo
# Date: 22/12/21 15:47
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import os

SENSOR_COLS = ['sensor_type', 'sensor_name']
APIPARAM_COLS = ['sensor_id', 'ch_key', 'ch_id', 'ch_name', 'last_acquisition']
GEOLOCATION_COLS = ['sensor_id', 'valid_from', 'geom']


from airquality.sqltable import FilterSQLTable, SQLTable
from airquality.sqldict import MutableSQLDict
from airquality.dbadapter import DBAdapterABC


class PurpleairFactory(object):

    def __init__(self, personality: str, dbadapter: DBAdapterABC, options=()):
        self.personality = personality
        self.dbadapter = dbadapter
        self.options = options
        self._url_template = ""

    @property
    def url_template(self) -> str:
        if not self._url_template:
            self._url_template = os.environ['purpleair_url']
        return self._url_template

    @property
    def sensor_table(self) -> FilterSQLTable:
        return FilterSQLTable(table_name="sensor", pkey="id", selected_cols=SENSOR_COLS, filter_col="sensor_type", filter_val="purpleair")

    @property
    def sensor_dict(self) -> MutableSQLDict:
        return MutableSQLDict(table=self.sensor_table, dbadapter=self.dbadapter)

    @property
    def apiparam_table(self) -> SQLTable:
        return SQLTable(table_name="api_param", pkey="id", selected_cols=APIPARAM_COLS)

    @property
    def apiparam_dict(self) -> MutableSQLDict:
        return MutableSQLDict(table=self.apiparam_table, dbadapter=self.dbadapter)

    @property
    def geolocation_table(self) -> SQLTable:
        return SQLTable(table_name="sensor_at_location", pkey="id", selected_cols=GEOLOCATION_COLS)

    @property
    def geolocation_dict(self) -> MutableSQLDict:
        return MutableSQLDict(table=self.geolocation_table, dbadapter=self.dbadapter)
