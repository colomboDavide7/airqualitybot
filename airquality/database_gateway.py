######################################################
#
# Author: Davide Colombo
# Date: 30/12/21 15:01
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from airquality.response_builder import AddFixedSensorResponseBuilder, AddMobileMeasureResponseBuilder
from airquality.database_adapter import DatabaseAdapter
from airquality.apiparam import APIParam
from typing import Set, Dict, List
from datetime import datetime


class DatabaseGateway(object):
    """
    An *object* class that moderates the interaction between the system and the database.
    """

    def __init__(self, dbadapter: DatabaseAdapter):
        self.dbadapter = dbadapter

    def get_existing_sensor_names_of_type(self, sensor_type: str) -> Set[str]:
        rows = self.dbadapter.fetchall(f"SELECT sensor_name FROM level0_raw.sensor WHERE sensor_type ILIKE '%{sensor_type}%';")
        return {row[0] for row in rows}

    def get_max_sensor_id_plus_one(self) -> int:
        row = self.dbadapter.fetchone("SELECT MAX(id) FROM level0_raw.sensor;")
        return 1 if row[0] is None else row[0] + 1

    def insert_sensors(self, responses: AddFixedSensorResponseBuilder):
        sensor_query = "INSERT INTO level0_raw.sensor VALUES "
        apiparam_query = "INSERT INTO level0_raw.sensor_api_param (sensor_id, ch_key, ch_id, ch_name, last_acquisition) VALUES "
        geolocation_query = "INSERT INTO level0_raw.sensor_at_location (sensor_id, valid_from, geom) VALUES "
        for response in responses:
            sensor_query += response.sensor_record + ','
            apiparam_query += response.apiparam_record + ','
            geolocation_query += response.geolocation_record + ','

        self.dbadapter.execute(f"{sensor_query.strip(',')}; {apiparam_query.strip(',')}; {geolocation_query.strip(',')};")

    def get_measure_param_owned_by(self, owner: str) -> Dict[str, int]:
        rows = self.dbadapter.fetchall(f"SELECT id, param_code FROM level0_raw.measure_param WHERE param_owner ILIKE '%{owner}%';")
        return {code: ident for ident, code in rows}

    def insert_mobile_sensor_measures(self, responses: AddMobileMeasureResponseBuilder):
        measure_query = "INSERT INTO level0_raw.mobile_measurement (packet_id, param_id, param_value, timestamp, geom) VALUES "
        measure_query += ','.join(resp.measure_record for resp in responses)
        self.dbadapter.execute(f"{measure_query};")

    def update_last_acquisition(self, timestamp: str, sensor_id: int, ch_name: str):
        self.dbadapter.execute(
            f"UPDATE level0_raw.sensor_api_param SET last_acquisition = '{timestamp}' "
            f"WHERE sensor_id = {sensor_id} AND ch_name = '{ch_name}';"
        )

    def get_apiparam_of_type(self, sensor_type: str) -> List[APIParam]:
        rows = self.dbadapter.fetchall(
            "SELECT a.sensor_id, a.ch_key, a.ch_id, a.ch_name, a.last_acquisition FROM level0_raw.sensor_api_param AS a "
            f"INNER JOIN level0_raw.sensor AS s ON s.id = a.sensor_id WHERE s.sensor_type ILIKE '%{sensor_type}%';"
        )
        return [
            APIParam(sensor_id=sid, api_key=key, api_id=ident, ch_name=name, last_acquisition=last)
            for sid, key, ident, name, last in rows
        ]

    def get_max_mobile_packet_id_plus_one(self) -> int:
        row = self.dbadapter.fetchone("SELECT MAX(packet_id) FROM level0_raw.mobile_measurement;")
        return 1 if row[0] is None else row[0] + 1

    def get_last_acquisition_of_sensor_channel(self, sensor_id: int, ch_name: str) -> datetime:
        return self.dbadapter.fetchone(
            f"SELECT last_acquisition FROM level0_raw.sensor_api_param WHERE sensor_id = {sensor_id} AND ch_name = '{ch_name}';"
        )

    def __repr__(self):
        return f"{type(self).__name__}(dbadapter={self.dbadapter!r})"
