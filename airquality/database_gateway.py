######################################################
#
# Author: Davide Colombo
# Date: 30/12/21 15:01
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from airquality.response_builder import AddFixedSensorResponseBuilder
from airquality.database_adapter import DatabaseAdapter
from typing import Set


class DatabaseGateway(object):
    """
    An *object* class that moderates the interaction between the system and the database.
    """

    def __init__(self, dbadapter: DatabaseAdapter):
        self.dbadapter = dbadapter

    def get_existing_sensor_names_of_type(self, sensor_type: str) -> Set[str]:
        rows = self.dbadapter.fetchall(f"SELECT sensor_name FROM level0_raw.sensor WHERE sensor_type ILIKE '%{sensor_type}%';")
        return {row[0] for row in rows}

    def get_start_sensor_id(self) -> int:
        row = self.dbadapter.fetchone("SELECT MAX(id) FROM level0_raw.sensor;")
        return 1 if row is None else row[0] + 1

    def insert_sensors(self, responses: AddFixedSensorResponseBuilder):
        sensor_query = "INSERT INTO level0_raw.sensor VALUES "
        apiparam_query = "INSERT INTO level0_raw.sensor_api_param (sensor_id, ch_key, ch_id, ch_name, last_acquisition) VALUES "
        geolocation_query = "INSERT INTO level0_raw.sensor_at_location (sensor_id, valid_from, geom) VALUES "
        for response in responses:
            sensor_query += response.sensor_record + ','
            apiparam_query += response.apiparam_record + ','
            geolocation_query += response.geolocation_record + ','

        self.dbadapter.execute(f"{sensor_query.strip(',')}; {apiparam_query.strip(',')}; {geolocation_query.strip(',')};")

    def __repr__(self):
        return f"{type(self).__name__}(dbadapter={self.dbadapter!r})"
