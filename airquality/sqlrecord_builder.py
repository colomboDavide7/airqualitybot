######################################################
#
# Author: Davide Colombo
# Date: 29/12/21 18:54
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from datetime import datetime
from airquality.response import AddFixedSensorResponse
from airquality.sqlrecord import FixedSensorSQLRecord

SQL_TIMESTAMP_FTM = "%Y-%m-%d %H:%M:%S"
POSTGIS_POINT = "POINT({lon} {lat})"
ST_GEOM_FROM_TEXT = "ST_GeomFromText('{geom}', {srid})"


class FixedSensorSQLRecordBuilder(object):

    def __init__(self, response: AddFixedSensorResponse, sensor_id: int):
        self.response = response
        self.sensor_id = sensor_id

    def build_sqlrecord(self) -> FixedSensorSQLRecord:
        sensor_record = f"({self.sensor_id}, '{self.response.type}', '{self.response.name}')"
        apiparam_record = ','.join(f"({self.sensor_id}, '{ch.api_key}', '{ch.api_id}', '{ch.channel_name}', '{ch.last_acquisition}')"
                                   for ch in self.response.channels)

        valid_from = datetime.now().strftime(SQL_TIMESTAMP_FTM)
        point = POSTGIS_POINT.format(lon=self.response.geolocation.longitude, lat=self.response.geolocation.latitude)
        geom = ST_GEOM_FROM_TEXT.format(geom=point, srid=26918)
        geolocation_record = f"({self.sensor_id}, '{valid_from}', NULL, {geom})"

        return FixedSensorSQLRecord(
            sensor_record=sensor_record,
            apiparam_record=apiparam_record,
            geolocation_record=geolocation_record
        )
