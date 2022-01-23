# ======================================
# @author:  Davide Colombo
# @date:    2022-01-23, dom, 15:09
# ======================================
from dataclasses import dataclass


@dataclass
class SensorIdentity(object):
    sensor_id: int                      # the sensor's unique id.
    sensor_name: str                    # the sensor's name.
    sensor_lat: float = None            # the sensor's latitude in decimal degrees (if fixed sensor).
    sensor_lng: float = None            # the sensor's longitude in decimal degrees (if fixed sensor).
