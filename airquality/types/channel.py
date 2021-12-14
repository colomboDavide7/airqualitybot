######################################################
#
# Author: Davide Colombo
# Date: 26/11/21 10:20
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.types.timestamp as ts


class Channel:

    def __init__(self, sensor_id: int, ch_id: str, ch_key: str, ch_name: str, last_acquisition: ts.SQLTimestamp):
        self.sensor_id = sensor_id
        self.ch_id = ch_id
        self.ch_key = ch_key
        self.ch_name = ch_name
        self.last_acquisition = last_acquisition
