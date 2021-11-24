#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 10:29
# @Description: this script defines a class for dynamically build valid rec queries. The query are read from the
#               'properties/query.json' file.
#
#################################################
from typing import List
import airquality.file.structured.json as struct
import airquality.database.rec.baserec as baserec


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

    ################################ INSERT MOBILE MEASUREMENTS ################################
    def insert_mobile_measurements(self, sensor_id: int, channel: str, values: List[str]) -> str:
        query = ""
        query += self.__insert_into_mobile_measurements(values)
        last_ts = values[-1].split(', ')[3]
        query += self.__update_last_acquisition(sensor_id=sensor_id, channel_name=channel, last_timestamp=last_ts)
        return query

    ################################ INSERT STATION MEASUREMENTS ################################
    def insert_station_measurements(self, sensor_id: int, channel: str, values: List[str]):
        query = ""
        query += self.__insert_into_station_measurements(values)
        last_ts = values[-1].split(',')[4].strip(')')
        query += self.__update_last_acquisition(sensor_id=sensor_id, channel_name=channel, last_timestamp=last_ts)
        return query

    ################################ UPDATE SENSOR AT LOCATION ################################
    def update_locations(self, sensor_at_loc_values: str, update_info: List[baserec.ParamIDTimestamp]) -> str:
        query = self.__update_valid_to_timestamp(update_info)
        query += self.__insert_location_values(sensor_at_loc_values)
        return query

    ################################ INITIALIZE SENSORS ################################
    def initialize_sensors(self, sensor_values: str, api_param_values: str, sensor_at_loc_values: str):
        query = self.__insert_into_sensor(sensor_values)
        query += self.__insert_into_api_param(api_param_values)
        query += self.__insert_location_values(sensor_at_loc_values)
        return query

    ################################ PRIVATE METHODS ################################
    def __insert_into_mobile_measurements(self, values: List[str]) -> str:
        query = self.query_file.i1
        query += ','.join(f"{v}" for v in values)
        return query.strip(',') + ';'

    def __insert_into_station_measurements(self, values: List[str]) -> str:
        query = self.query_file.i2
        query += ','.join(f"{v}" for v in values)
        return query.strip(',') + ';'

    def __insert_into_sensor(self, values: str) -> str:
        query = self.query_file.i3
        query += values
        return query.strip(',') + ';'

    def __insert_into_api_param(self, values: str) -> str:
        query = self.query_file.i4
        query += values
        return query.strip(',') + ';'

    def __insert_location_values(self, values: str) -> str:
        query = self.query_file.i5
        query += values
        return query.strip(',') + ';'

    def __update_valid_to_timestamp(self, update_info: List[baserec.ParamIDTimestamp]):
        query = ""
        for info in update_info:
            query += self.query_file.u1.format(ts=info.timestamp.get_formatted_timestamp(), sens_id=info.id)
        return query

    def __update_last_acquisition(self, sensor_id: int, channel_name: str, last_timestamp):
        return self.query_file.u2.format(ts=last_timestamp, sensor_id=sensor_id, channel=channel_name)
