######################################################
#
# Author: Davide Colombo
# Date: 25/11/21 15:10
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.api2db.adptype as adptype


class StationInfoRecord:

    def __init__(self, station_info: adptype.StationInfo, sensor_id: int):
        self.station_info = station_info
        self.sensor_id = sensor_id

    def get_sensor_value(self) -> str:
        return f"({self.sensor_id}, '{self.station_info.sensor_name}', '{self.station_info.sensor_type}')"

    def get_channel_param_value(self) -> str:
        return ','.join(
            f"({self.sensor_id}, '{c.ch_key}', '{c.ch_id}', '{c.ch_name}', '{c.last_acquisition.get_formatted_timestamp()}')"
            for c in self.station_info.ch_param
        )

    def get_geolocation_value(self) -> str:
        return f"({self.sensor_id}, " \
               f"'{self.station_info.geolocation.timestamp.get_formatted_timestamp()}', " \
               f"{self.station_info.geolocation.geometry.geom_from_text()})"
