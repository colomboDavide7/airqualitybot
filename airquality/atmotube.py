######################################################
#
# Author: Davide Colombo
# Date: 27/12/21 19:25
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import itertools
from typing import Dict, Set
from airquality.dblookup import SensorAPIParam
from airquality.dbadapter import DBAdapterABC
from airquality.response import AtmotubeAPIResponses
from airquality.respfilter import AtmotubeFilteredResponses
from airquality.sqlrecord import AtmotubeSQLRecords
from airquality.iterableurl import AtmotubeIterableURL


class Atmotube:

    def __init__(self, personality: str, url_template: str, dbadapter: DBAdapterABC, **url_options):
        self.url_template = url_template
        self.url_options = url_options
        self.personality = personality
        self.dbadapter = dbadapter
        self._measure_param = {}

    @property
    def start_packet_id(self) -> int:
        row = self.dbadapter.fetch_one(f"SELECT MAX(packet_id) FROM level0_raw.mobile_measurement;")
        return 1 if row[0] is None else row[0] + 1

    @property
    def measure_param(self) -> Dict[str, int]:
        if not self._measure_param:
            rows = self.dbadapter.fetch_all(
                f"SELECT param_code, id FROM level0_raw.measure_param WHERE param_owner ILIKE '%{self.personality}%';")
            self._measure_param = {param_code: param_id for param_code, param_id in rows}
        return self._measure_param

    @property
    def apiparam(self) -> Set[SensorAPIParam]:
        rows = self.dbadapter.fetch_all(
            "SELECT a.id, a.sensor_id, a.ch_key, a.ch_id, a.ch_name, a.last_acquisition "
            "FROM level0_raw.sensor_api_param AS a INNER JOIN level0_raw.sensor AS s ON s.id = a.sensor_id "
            f"WHERE s.sensor_type ILIKE '%{self.personality}%';")
        for row in rows:
            yield SensorAPIParam(*row)

    def execute(self):
        for param in self.apiparam:
            self.url_options.update(param.database_url_param)
            url = self.url_template.format(**self.url_options)
            urls = AtmotubeIterableURL(url=url, begin=param.last_acquisition)
            for url in urls:
                api_responses = AtmotubeAPIResponses(url=url)
                filtered_responses = AtmotubeFilteredResponses(responses=api_responses, filter_ts=param.last_acquisition)
                sql_records = AtmotubeSQLRecords(responses=filtered_responses, measure_param=self.measure_param)
                if len(sql_records) > 0:
                    query = self.build_query(sql_records=sql_records, sensor_id=param.sensor_id)
                    self.dbadapter.execute(query)

    def build_query(self, sql_records: AtmotubeSQLRecords, sensor_id: int) -> str:
        measurement_query = "INSERT INTO level0_raw.mobile_measurement (packet_id, param_id, param_value, timestamp, geom) VALUES "
        apiparam_query = "UPDATE level0_raw.sensor_api_param SET last_acquisition = '{timestamp}' WHERE sensor_id= %s;" % sensor_id

        packet_id = itertools.count(self.start_packet_id)
        measurement_query += ','.join(record.measurement.format(packet_id=next(packet_id)) for record in sql_records)
        return f"{measurement_query.strip(',')}; {apiparam_query.format(timestamp=sql_records[-1].measured_at)};"
