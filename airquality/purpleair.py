######################################################
#
# Author: Davide Colombo
# Date: 28/12/21 11:06
# Description: INSERT HERE THE DESCRIPTION
#
#####################################################
import itertools
from typing import Set
from airquality.dbadapter import DBAdapterABC
from airquality.response import PurpleairAPIResponses
from airquality.respfilter import PurpleairFilteredResponses
from airquality.sqlrecord import PurpleairSQLRecords


class Purpleair(object):

    def __init__(self, personality: str, url: str, dbadapter: DBAdapterABC):
        self.url = url
        self.personality = personality
        self.dbadapter = dbadapter

    @property
    def start_sensor_id(self):
        row = self.dbadapter.fetch_one(f"SELECT MAX(id) FROM level0_raw.sensor;")
        return 1 if row[0] is None else row[0] + 1

    @property
    def database_sensor_names(self) -> Set[str]:
        rows = self.dbadapter.fetch_all(
            f"SELECT sensor_name FROM level0_raw.sensor WHERE sensor_type ILIKE '%{self.personality}%'")
        return {row[0] for row in rows}

    def execute(self):
        api_responses = PurpleairAPIResponses(url=self.url)
        filtered_responses = PurpleairFilteredResponses(responses=api_responses, database_sensor_names=self.database_sensor_names)
        sql_records = PurpleairSQLRecords(responses=filtered_responses)
        if len(sql_records) > 0:
            query = self.build_query(sql_records)
            self.dbadapter.execute(query)

    def build_query(self, sql_records: PurpleairSQLRecords) -> str:
        sensor_query = "INSERT INTO level0_raw.sensor VALUES "
        apiparam_query = "INSERT INTO level0_raw.sensor_api_param (sensor_id, ch_key, ch_id, ch_name, last_acquisition) VALUES "
        location_query = "INSERT INTO level0_raw.sensor_at_location (sensor_id, valid_from, geom) VALUES "

        sensor_id = itertools.count(self.start_sensor_id)
        for item in sql_records:
            sid = next(sensor_id)
            sensor_query += item.sensor.format(sensor_id=sid)
            apiparam_query += item.apiparam.format(sensor_id=sid)
            location_query += item.sensor_location.format(sensor_id=sid)

        return f"{sensor_query.strip(',')}; {apiparam_query.strip(',')}; {location_query.strip(',')};"

    def __repr__(self):
        return f"{type(self).__name__}(personality={self.personality}, url=XXX, dbadapter={self.dbadapter})"
