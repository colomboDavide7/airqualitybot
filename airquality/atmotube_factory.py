######################################################
#
# Author: Davide Colombo
# Date: 22/12/21 16:40
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
SENSOR_COLS = ['sensor_type', 'sensor_name']
APIPARAM_COLS = ['sensor_id', 'ch_key', 'ch_id', 'ch_name', 'last_acquisition']
MEASURE_PARAM_COLS = ['param_code', 'param_name', 'param_unit']
MOBILE_MEASURE_COLS = ['param_id', 'param_value', 'timestamp', 'geom']


from airquality.dbadapter import DBAdapterABC
from airquality.sqltable import SQLTable, FilterSQLTable, JoinSQLTable
from airquality.sqldict import HeavyweightMutableSQLDict, FrozenSQLDict


class AtmotubeFactory(object):

    def __init__(self, personality: str, dbadapter: DBAdapterABC, options=()):
        self.personality = personality
        self.dbadapter = dbadapter
        self.options = options

    @property
    def mobile_table(self) -> SQLTable:
        return SQLTable(table_name="mobile_measurement", pkey="id", selected_cols=MOBILE_MEASURE_COLS)

    @property
    def mobile_dict(self) -> HeavyweightMutableSQLDict:
        return HeavyweightMutableSQLDict(table=self.mobile_table, dbadapter=self.dbadapter)

    @property
    def measure_param_table(self) -> FilterSQLTable:
        return FilterSQLTable(
            table_name="measure_param", pkey="id", selected_cols=MEASURE_PARAM_COLS, filter_col="param_name", filter_val="atmotube"
        )

    @property
    def measure_param_dict(self) -> FrozenSQLDict:
        return FrozenSQLDict(table=self.measure_param_table, dbadapter=self.dbadapter)

    @property
    def apiparam_table(self) -> JoinSQLTable:
        join_table = FilterSQLTable(
            table_name="sensor", pkey="id", selected_cols=SENSOR_COLS, filter_col="sensor_type", filter_val="atmotube", alias="s"
        )
        return JoinSQLTable(
            table_name="api_param", pkey="id", fkey="sensor_id", selected_cols=APIPARAM_COLS, alias="a", join_table=join_table
        )
