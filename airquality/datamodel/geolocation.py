# ======================================
# @author:  Davide Colombo
# @date:    2022-01-27, gio, 16:44
# ======================================
from typing import Tuple


class Geolocation(object):
    """
    A class that defines the datastructure for a raw geolocation instance.
    """

    def __init__(self, row: Tuple):
        self._longitude = row[0]
        self._latitude = row[1]

    @property
    def latitude(self) -> float:
        return self._latitude

    @property
    def longitude(self) -> float:
        return self._longitude

    def __repr__(self):
        return f"{type(self).__name__}(longitude={self._longitude}, latitude={self._latitude})"
