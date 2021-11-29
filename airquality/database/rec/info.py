######################################################
#
# Author: Davide Colombo
# Date: 25/11/21 15:10
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.logger.loggable as log
import airquality.types.timestamp as ts
import airquality.types.postgis as pgis


class InfoRecordBuilder(log.Loggable):

    def __init__(self, log_filename="log"):
        super(InfoRecordBuilder, self).__init__(log_filename=log_filename)
        self.sensor_id = None

    def with_sensor_id(self, sensor_id: int):
        self.sensor_id = sensor_id
        return self

    def get_sensor_value(self, sensor_name: str, sensor_type: str) -> str:
        return f"({self.sensor_id}, '{sensor_type}', '{sensor_name}'),"

    def get_channel_param_value(self, ident: str, key: str, name: str, timest: ts.Timestamp) -> str:
        return f"({self.sensor_id}, '{key}', '{ident}', '{name}', '{timest.get_formatted_timestamp()}')"

    def get_geolocation_value(self, timest: ts.Timestamp, geometry: pgis.PostgisGeometry) -> str:
        return f"({self.sensor_id}, '{timest.get_formatted_timestamp()}', {geometry.geom_from_text()}),"
