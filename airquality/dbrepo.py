######################################################
#
# Author: Davide Colombo
# Date: 23/12/21 19:41
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
SENSOR_COLS = ['sensor_type', 'sensor_name']
GEOLOCATION_COLS = ['sensor_id', 'valid_from', 'geom']
APIPARAM_COLS = ['sensor_id', 'ch_key', 'ch_id', 'ch_name', 'last_acquisition']
MEASURE_PARAM_COLS = ['param_owner', 'param_code', 'param_name', 'param_unit']
STATION_MEASURE_COLS = ['packet_id', 'param_id', 'sensor_id', 'param_value', 'timestamp']
MOBILE_MEASURE_COLS = ['packet_id', 'param_id', 'param_value', 'timestamp', 'geom']

from airquality.sqltable import SQLTableABC, FilterSQLTable, SQLTable, JoinSQLTable


class DBRepository(object):

    @staticmethod
    def filtered_sensor_table(requested_type: str) -> FilterSQLTable:
        return FilterSQLTable(table_name="sensor", pkey="id", selected_cols=SENSOR_COLS, filter_col="sensor_type", filter_val=requested_type)

    @staticmethod
    def apiparam_table() -> SQLTable:
        return SQLTable(table_name="sensor_api_param", pkey="id", selected_cols=APIPARAM_COLS)

    @staticmethod
    def geolocation_table() -> SQLTable:
        return SQLTable(table_name="sensor_at_location", pkey="id", selected_cols=GEOLOCATION_COLS)

    @staticmethod
    def filtered_measure_param_table(requested_param: str) -> FilterSQLTable:
        return FilterSQLTable(
            table_name="measure_param", pkey="id", selected_cols=MEASURE_PARAM_COLS, filter_col="param_owner", filter_val=requested_param
        )

    @staticmethod
    def joined_sensor_api_param_table(join_table: SQLTableABC) -> JoinSQLTable:
        return JoinSQLTable(
            table_name="sensor_api_param", pkey="id", fkey="sensor_id", selected_cols=APIPARAM_COLS, alias="a", join_table=join_table
        )

    @staticmethod
    def station_measure_table() -> SQLTable:
        return SQLTable(table_name="station_measurement", pkey="id", selected_cols=STATION_MEASURE_COLS)

    @staticmethod
    def mobile_measure_table() -> SQLTable:
        return SQLTable(table_name="mobile_measurement", pkey="id", selected_cols=MOBILE_MEASURE_COLS)

    @staticmethod
    def filtered_service_table(requested_type: str) -> FilterSQLTable:
        return FilterSQLTable(table_name="service", pkey="id", selected_cols=['service_name'], filter_col="service_name", filter_val=requested_type)

    @staticmethod
    def geoarea_table():
        return SQLTable(table_name="geographical_area", pkey="id", selected_cols=['postal_code'])
