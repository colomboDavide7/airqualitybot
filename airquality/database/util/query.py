#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 10:29
# @Description: this script defines a class for dynamically build valid rec queries. The query are read from the
#               'properties/query.json' file.
#
#################################################
from typing import List
import airquality.database.rec.mobile as mbmeasrec
import airquality.database.rec.info as stinforec
import airquality.database.rec.station as stmeasrec
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

    ################################ INSERT MOBILE MEASUREMENTS ################################
    def insert_mobile_measurements(self, records: List[mbmeasrec.MobileMeasureRecord]) -> str:
        mobile_measure_values = ','.join(f"{r.get_mobile_measurement_value()}" for r in records)
        return f"{self.query_file.i1} {mobile_measure_values};"

    def update_last_acquisition(self, sensor_id: int, channel_name: str, last_timestamp: str):
        return self.query_file.u2.format(ts=last_timestamp, sensor_id=sensor_id, channel=channel_name)

    ################################ INSERT STATION MEASUREMENTS ################################
    def insert_station_measurements(self, records: List[stmeasrec.StationMeasureRecord]):
        station_measure_values = ','.join(f"{r.get_station_measurement_value()}" for r in records)
        return f"{self.query_file.i2} {station_measure_values};"

    ################################ INSERT LOCATIONS ################################
    def insert_locations(self, records: List[stinforec.SensorInfoRecord]) -> str:
        geolocation_values = ','.join(f"{r.get_geolocation_value()}" for r in records)
        return f"{self.query_file.i5} {geolocation_values};"

    def update_valid_to_timestamp(self, records: List[stinforec.SensorInfoRecord]):
        return ' '.join(self.query_file.u1.format(ts=r.api_adpt_resp.geolocation.timestamp.get_formatted_timestamp(),
                                                  sens_id=r.sensor_id) for r in records)

    ################################ INITIALIZE SENSORS ################################
    def initialize_sensors(self, records: List[stinforec.SensorInfoRecord]):
        sensor_values = ','.join(f"{r.get_sensor_value()}" for r in records)
        api_param_values = ','.join(f"{r.get_channel_param_value()}" for r in records)
        geolocation_values = ','.join(f"{r.get_geolocation_value()}" for r in records)

        query = f"{self.query_file.i3} {sensor_values};"
        query += f"{self.query_file.i4} {api_param_values};"
        query += f"{self.query_file.i5} {geolocation_values};"
        return query
