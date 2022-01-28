# ======================================
# @author:  Davide Colombo
# @date:    2022-01-23, dom, 15:09
# ======================================
from typing import Tuple


class SensorIdentity(object):
    def __init__(self, row: Tuple):
        self._sensor_id = row[0]
        self._sensor_name = row[1]
        self._longitude = row[2] if len(row) > 2 else None
        self._latitude = row[3] if len(row) > 3 else None

    @property
    def sensor_id(self) -> int:
        return self._sensor_id

    @property
    def sensor_name(self) -> str:
        return self._sensor_name

    @property
    def sensor_lng(self) -> float:
        return self._longitude

    @property
    def sensor_lat(self) -> float:
        return self._latitude

    def __repr__(self):
        return f"{type(self).__name__}"
