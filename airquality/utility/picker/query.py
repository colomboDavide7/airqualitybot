#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 10:29
# @Description: this script defines a class for dynamically build valid sql queries. The query are read from the
#               'properties/query.json' file.
#
#################################################
from typing import Dict, Any, List
import airquality.data.builder.sql as sb
from airquality.core.constants.shared_constants import EXCEPTION_HEADER


class QueryPicker:

    def __init__(self, parsed_query_data: Dict[str, Any]):
        self.parsed_query_data = parsed_query_data

    ################################ METHODS THAT RETURN SELECT QUERY ################################
    def select_max_sensor_id(self) -> str:
        query_id = "s1"
        self.search_query_id(query_id)
        return self.parsed_query_data[query_id]

    def select_api_param_from_sensor_id(self) -> str:
        query_id = "s2"
        self.search_query_id(query_id)
        return self.parsed_query_data[query_id]

    def select_sensor_ids_from_personality(self, personality: str) -> str:
        query_id = "s3"
        self.search_query_id(query_id)
        return self.parsed_query_data[query_id].format(personality=personality)

    def select_sensor_name_from_personality(self, personality: str) -> str:
        query_id = "s4"
        self.search_query_id(query_id)
        return self.parsed_query_data[query_id].format(personality=personality)

    def select_measure_param_from_personality(self, personality: str) -> str:
        query_id = "s5"
        self.search_query_id(query_id)
        return self.parsed_query_data[query_id].format(personality=personality)

    def select_active_sensor_location(self, personality: str) -> str:
        query_id = "s6"
        self.search_query_id(query_id)
        return self.parsed_query_data[query_id].format(personality=personality)

    def select_sensor_name_id_mapping_from_personality(self, personality: str) -> str:
        query_id = "s7"
        self.search_query_id(query_id)
        return self.parsed_query_data[query_id].format(personality=personality)

    ################################ METHODS THAT RETURN INSERT QUERY ################################

    def insert_into_mobile_measurements(self) -> str:
        query_id = "i1"
        self.search_query_id(query_id)
        return self.parsed_query_data[query_id]

    def insert_into_station_measurements(self) -> str:
        query_id = "i2"
        self.search_query_id(query_id)
        return self.parsed_query_data[query_id]

    def insert_into_sensor(self, values: List[sb.SensorSQLBuilder]) -> str:
        query_id = "i3"
        self.search_query_id(query_id)
        query = self.parsed_query_data[query_id]
        for value in values:
            query += value.sql() + ','
        return query.strip(',') + ';'

    def insert_into_api_param(self, values: List[sb.APIParamSQLBuilder]) -> str:
        query_id = "i4"
        self.search_query_id(query_id)
        query = self.parsed_query_data[query_id]
        for value in values:
            query += value.sql() + ','
        return query.strip(',') + ';'

    def insert_into_sensor_at_location(self, values: List[sb.SensorAtLocationSQLBuilder]) -> str:
        query_id = "i5"
        self.search_query_id(query_id)
        query = self.parsed_query_data[query_id]
        for value in values:
            query += value.sql() + ','
        return query.strip(',') + ';'

    ################################ METHODS THAT RETURN UPDATE QUERY ################################

    def update_last_packet_date_atmotube(self, ts: str, sensor_id: int) -> str:
        query_id = "u1"
        self.search_query_id(query_id)
        query = self.parsed_query_data[query_id].format(par_val=ts, sens_id=sensor_id, par_name="date")
        return query

    def update_valid_to_location_timestamp(self, sensor_id: int, ts: str) -> str:
        query_id = "u2"
        self.search_query_id(query_id)
        return self.parsed_query_data[query_id].format(ts=ts, sens_id=sensor_id)

    def update_last_channel_acquisition_timestamp(self, sensor_id: str, ts: str, param2update: str) -> str:
        query_id = "u3"
        self.search_query_id(query_id)
        return self.parsed_query_data[query_id].format(ts=ts, sens_id=sensor_id, par_name=param2update)

    ################################ METHOD THAT RAISES EXCEPTION ################################
    def search_query_id(self, query_id: str):
        if query_id not in self.parsed_query_data.keys():
            raise SystemExit(
                f"{EXCEPTION_HEADER} {QueryPicker.__name__} bad 'query.json' file structure => missing key='{query_id}'."
            )
