######################################################
#
# Author: Davide Colombo
# Date: 26/11/21 11:08
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List
import airquality.types.channel as chtype
import airquality.types.geolocation as geotype


class SensorInfoResponse:

    def __init__(self, sensor_name: str, sensor_type: str, channels: List[chtype.Channel], geolocation: geotype.Geolocation):
        self.sensor_name = sensor_name
        self.sensor_type = sensor_type
        self.channels = channels
        self.geolocation = geolocation

    def sensor2sql(self, sensor_id: int) -> str:
        return f"({sensor_id}, '{self.sensor_type}', '{self.sensor_name}'),"

    def apiparam2sql(self, sensor_id: int) -> str:
        return ','.join(f"({sensor_id}, '{c.ch_key}', '{c.ch_id}', '{c.ch_name}', '{c.last_acquisition.ts}')"
                        for c in self.channels) + ','

    def geo2sql(self, sensor_id: int) -> str:
        return f"({sensor_id}, '{self.geolocation.timestamp.ts}', {self.geolocation.geometry.geom_from_text()}),"
