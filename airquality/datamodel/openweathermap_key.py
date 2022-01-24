######################################################
#
# Author: Davide Colombo
# Date: 03/01/22 20:52
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from dataclasses import dataclass


@dataclass
class OpenweathermapKey(object):
    """
    A *dataclass* that defines the raw datastructure for the openweathermap API key queried from the database.
    """

    key_value: str                      # The openweathermap's API key.
    done_requests_per_minute: int       # The number of requests in the last minute done using this key.
    max_requests_per_minute: int        # The maximum number of requests that can be done in a minute.

    def __repr__(self):
        return f"{type(self).__name__}(key_value=XXX, done_requests_per_minute={self.done_requests_per_minute}, " \
               f"max_requests_per_minute={self.max_requests_per_minute})"
