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
        self.api_adpt_resp = info_resp
        self.sensor_id = sensor_id

    def get_sensor_value(self) -> str:
        return f"({self.sensor_id}, '{self.api_adpt_resp.sensor_type}', '{self.api_adpt_resp.sensor_name}')"

    def get_channel_param_value(self) -> str:
        return ','.join(
            f"({self.sensor_id}, '{c.ch_key}', '{c.ch_id}', '{c.ch_name}', '{c.last_acquisition.get_formatted_timestamp()}')"
            for c in self.api_adpt_resp.channels
        )

    def get_geolocation_value(self) -> str:
        return f"({self.sensor_id}, " \
               f"'{self.api_adpt_resp.geolocation.timestamp.get_formatted_timestamp()}', " \
               f"{self.api_adpt_resp.geolocation.geometry.geom_from_text()})"
