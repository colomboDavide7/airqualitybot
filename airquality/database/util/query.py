#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 10:29
# @Description: this script defines a class for dynamically build valid rec queries. The query are read from the
#               'properties/query.json' file.
#
#################################################
import airquality.file.structured.json as struct


class QueryBuilder:

    def __init__(self, query_file: struct.JSONFile):
        self.query_file = query_file

    ################################ METHODS THAT RETURN SELECT QUERY STATEMENT ################################
    def select_max_sensor_id(self) -> str:
        return self.query_file.s1

    def select_api_param_from_sensor_id(self, sensor_id) -> str:
        return self.query_file.s2.format(sensor_id=sensor_id)

    def select_sensor_id_name_from_type(self, sensor_type: str) -> str:
        return self.query_file.s3.format(personality=sensor_type)

    def select_sensor_names_from_sensor_type(self, sensor_type: str) -> str:
        return self.query_file.s4.format(personality=sensor_type)

    def select_measure_param_from_sensor_type(self, sensor_type: str) -> str:
        return self.query_file.s5.format(personality=sensor_type)

    def select_location_from_sensor_id(self, sensor_id: int) -> str:
        return self.query_file.s6.format(sensor_id=sensor_id)

    def select_sensor_name_id_mapping_from_sensor_type(self, sensor_type: str) -> str:
        return self.query_file.s7.format(personality=sensor_type)

    def select_last_acquisition(self, channel: str, sensor_id: int):
        return self.query_file.s8.format(sensor_id=sensor_id, channel=channel)

    def select_max_mobile_record_id(self):
        return self.query_file.s9

    def select_max_station_record_id(self):
        return self.query_file.s10

    def select_channel_info_from_sensor_id(self, sensor_id: int):
        return self.query_file.s11.format(sensor_id=sensor_id)

    def select_sensor_id_from_type(self, type_: str):
        return self.query_file.s12.format(type=type_)

    ################################ INIT COMMAND QUERY ################################
    def build_initialize_sensor_query(self, sensor_values: str, api_param_values: str, geolocation_values: str):
        query = f"{self.query_file.i3} {sensor_values};"
        query += f"{self.query_file.i4} {api_param_values};"
        query += f"{self.query_file.i5} {geolocation_values};"
        return query

    ################################ UPDATE COMMAND QUERIES ################################
    def build_insert_sensor_location_query(self, geolocation_values: str) -> str:
        return f"{self.query_file.i5} {geolocation_values};"

    def build_update_location_validity_query(self, valid_to: str, sensor_id: int):
        return self.query_file.u1.format(ts=valid_to, sens_id=sensor_id)

    ################################ FETCH COMMAND QUERIES ################################
    def build_insert_mobile_measure_query(self, mobile_measure_values: str) -> str:
        return f"{self.query_file.i1} {mobile_measure_values};"

    def build_insert_station_measure_query(self, station_measure_values: str):
        return f"{self.query_file.i2} {station_measure_values};"

    def build_update_last_channel_acquisition_query(self, sensor_id: int, channel_name: str, last_timestamp: str):
        return self.query_file.u2.format(ts=last_timestamp, sensor_id=sensor_id, channel=channel_name)
