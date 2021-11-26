######################################################
#
# Author: Davide Colombo
# Date: 25/11/21 15:10
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.types.apiresp.inforesp as resp


class SensorInfoRecord:

    def __init__(self, info_resp: resp.SensorInfoResponse, sensor_id: int):
        self.response = info_resp
        self.sensor_id = sensor_id

    def get_sensor_value(self) -> str:
        return f"({self.sensor_id}, '{self.response.sensor_type}', '{self.response.sensor_name}')"

    def get_channel_param_value(self) -> str:
        return ','.join(
            f"({self.sensor_id}, '{c.ch_key}', '{c.ch_id}', '{c.ch_name}', '{c.last_acquisition.get_formatted_timestamp()}')"
            for c in self.response.channels
        )

    def get_geolocation_value(self) -> str:
        return f"({self.sensor_id}, " \
               f"'{self.response.geolocation.timestamp.get_formatted_timestamp()}', " \
               f"{self.response.geolocation.geometry.geom_from_text()})"
