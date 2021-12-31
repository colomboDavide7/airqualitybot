######################################################
#
# Author: Davide Colombo
# Date: 31/12/21 12:41
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from dataclasses import dataclass
from datetime import datetime


@dataclass
class APIParam(object):
    """
    An *object* that represents the database sensor's API parameters data.
    """

    sensor_id: int                      # The unique identifier of a sensor within the database.
    api_key: str                        # The API key used to claim the ownership of the sensor when accessing data.
    api_id: str                         # The API id used together with the API key.
    ch_name: str                        # The name assigned to the channel associated to the API credentials.
    last_acquisition: datetime          # The timestamp of the last acquisition on the current channel.

    def __repr__(self):
        return f"{type(self).__name__}(sensor_id={self.sensor_id}, api_key=XXX, api_id=XXX, " \
               f"ch_name={self.ch_name}, last_acquisition={self.last_acquisition!s})"
