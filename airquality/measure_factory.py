######################################################
#
# Author: Davide Colombo
# Date: 23/12/21 09:05
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import os
from abc import ABC, abstractmethod
from airquality.dbadapter import DBAdapterABC
from airquality.sqltable import SQLTableABC, FilterSQLTable, JoinSQLTable
from airquality.sqldict import HeavyweightInsertSQLDict, FrozenSQLDict, MutableSQLDict

SENSOR_COLS = ['sensor_type', 'sensor_name']
MEASURE_PARAM_COLS = ['param_code', 'param_name', 'param_unit']
APIPARAM_COLS = ['sensor_id', 'ch_key', 'ch_id', 'ch_name', 'last_acquisition']


class MeasureFactory(ABC):

    def __init__(self, personality: str, dbadapter: DBAdapterABC, options=()):
        self.personality = personality
        self.dbadapter = dbadapter
        self.options = options

    @abstractmethod
    def measure_table(self) -> SQLTableABC:
        pass

    @property
    def url_template(self) -> str:
        return os.environ[f'{self.personality}_url']

    @property
    def measure_dict(self) -> HeavyweightInsertSQLDict:
        return HeavyweightInsertSQLDict(table=self.measure_table(), dbadapter=self.dbadapter)

    @property
    def measure_param_table(self) -> FilterSQLTable:
        return FilterSQLTable(
            table_name="measure_param", pkey="id", selected_cols=MEASURE_PARAM_COLS, filter_col="param_name", filter_val=self.personality
        )

    @property
    def measure_param_dict(self) -> FrozenSQLDict:
        return FrozenSQLDict(table=self.measure_param_table, dbadapter=self.dbadapter)

    @property
    def apiparam_table(self) -> JoinSQLTable:
        join_table = FilterSQLTable(
            table_name="sensor", pkey="id", selected_cols=SENSOR_COLS, filter_col="sensor_type", filter_val=self.personality, alias="s"
        )
        return JoinSQLTable(
            table_name="api_param", pkey="id", fkey="sensor_id", selected_cols=APIPARAM_COLS, alias="a", join_table=join_table
        )

    @property
    def apiparam_dict(self) -> MutableSQLDict:
        return MutableSQLDict(table=self.apiparam_table, dbadapter=self.dbadapter)
