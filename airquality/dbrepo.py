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
SERVICE_APIPARAM_COLS = ['api_key', 'n_requests']

from airquality.sqlcolumn_link import SQLColumnLink
from airquality.sqlsearch_link import SQLSearchLink
from airquality.sqlsearch import ILIKESearch, INSearch, EqualSearch
from airquality.sqlcolumn import SQLColumn, ST_X_Column, ST_Y_Column
from airquality.sqltable import SQLTableABC, FilterSQLTable, SQLTable, JoinSQLTable


class DBRepository(object):

    @staticmethod
    def filtered_sensor_table(requested_type: str) -> FilterSQLTable:
        ilike_search = ILIKESearch(search_column="sensor_type", search_value=requested_type)
        column_link = SQLColumnLink(columns=[SQLColumn(target_column=col) for col in SENSOR_COLS])
        return FilterSQLTable(table_name="sensor", pkey="id", selected_cols=column_link, search=ilike_search)

    @staticmethod
    def apiparam_table() -> SQLTable:
        column_link = SQLColumnLink(columns=[SQLColumn(target_column=col) for col in APIPARAM_COLS])
        return SQLTable(table_name="sensor_api_param", pkey="id", selected_cols=column_link)

    @staticmethod
    def geolocation_table() -> SQLTable:
        column_link = SQLColumnLink(columns=[SQLColumn(target_column=col) for col in GEOLOCATION_COLS])
        return SQLTable(table_name="sensor_at_location", pkey="id", selected_cols=column_link)

    @staticmethod
    def filtered_measure_param_table(requested_param: str) -> FilterSQLTable:
        ilike_search = ILIKESearch(search_column="param_owner", search_value=requested_param)
        column_link = SQLColumnLink(columns=[SQLColumn(target_column=col) for col in MEASURE_PARAM_COLS])
        return FilterSQLTable(
            table_name="measure_param", pkey="id", selected_cols=column_link, search=ilike_search,
        )

    @staticmethod
    def joined_sensor_api_param_table(join_table: SQLTableABC) -> JoinSQLTable:
        table_alias = "a"
        column_link = SQLColumnLink(columns=[SQLColumn(target_column=col, alias=table_alias) for col in APIPARAM_COLS])
        return JoinSQLTable(
            table_name="sensor_api_param", pkey="id", fkey="sensor_id", selected_cols=column_link, alias=table_alias, join_table=join_table
        )

    @staticmethod
    def station_measure_table() -> SQLTable:
        column_link = SQLColumnLink(columns=[SQLColumn(target_column=col) for col in STATION_MEASURE_COLS])
        return SQLTable(table_name="station_measurement", pkey="id", selected_cols=column_link)

    @staticmethod
    def mobile_measure_table() -> SQLTable:
        column_link = SQLColumnLink(columns=[SQLColumn(target_column=col) for col in MOBILE_MEASURE_COLS])
        return SQLTable(table_name="mobile_measurement", pkey="id", selected_cols=column_link)

    @staticmethod
    def filtered_service_table(requested_type: str) -> FilterSQLTable:
        table_alias = "s"
        column = SQLColumn(target_column='service_name')
        ilike_search = ILIKESearch(search_column="service_name", search_value=requested_type, alias=table_alias)
        return FilterSQLTable(table_name="service", pkey="id", selected_cols=column, search=ilike_search, alias=table_alias)

    @staticmethod
    def geoarea_table() -> SQLTable:
        column = SQLColumn(target_column='postal_code')
        return SQLTable(table_name="geographical_area", pkey="id", selected_cols=column)

    @staticmethod
    def filtered_geoarea_table(requested_cities="Pavia", country='IT') -> FilterSQLTable:
        search_city = EqualSearch(search_column="place_name", search_value="Pavia")
        search_country = EqualSearch(search_column='country_code', search_value="IT")
        search = SQLSearchLink(search_conditions=[search_city, search_country], link_keyword="AND")
        # in_search = INSearch(search_column="place_name", search_value=requested_cities)

        postgis_lat_column = ST_Y_Column(target_column="geom")
        postgis_lng_column = ST_X_Column(target_column="geom")
        column_link = SQLColumnLink(columns=[postgis_lat_column, postgis_lng_column])
        return FilterSQLTable(table_name="geographical_area", pkey="id", selected_cols=column_link, search=search)

    @staticmethod
    def joined_service_api_param(join_table: SQLTableABC) -> JoinSQLTable:
        table_alias = "a"
        column_link = SQLColumnLink(columns=[SQLColumn(target_column=col, alias=table_alias) for col in SERVICE_APIPARAM_COLS])
        return JoinSQLTable(
            table_name="service_api_param", pkey="id", fkey="service_id", selected_cols=column_link, alias=table_alias, join_table=join_table
        )

    # @staticmethod
    # def current_weather_table() -> :
