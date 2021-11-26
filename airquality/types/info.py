######################################################
#
# Author: Davide Colombo
# Date: 26/11/21 10:24
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List
import airquality.types.channel as ch
import airquality.types.geolocation as geo


class StationInfo:

    def __init__(self, sensor_name: str, sensor_type: str, ch_param: List[ch.Channel], geolocation: geo.Geolocation):
        self.sensor_name = sensor_name
        self.sensor_type = sensor_type
        self.ch_param = ch_param
        self.geolocation = geolocation
