######################################################
#
# Author: Davide Colombo
# Date: 25/11/21 12:02
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List, Union
import airquality.database.ext.postgis as pgis
import airquality.database.dtype.timestamp as ts
import airquality.database.op.sel.sel as sel


class Measure:

    def __init__(self, id_: int, value: str):
        self.param_id = id_
        self.param_val = value


class Geolocation:

    def __init__(self, timestamp: ts.Timestamp, geometry: pgis.PostgisGeometry):
        self.timestamp = timestamp
        self.geometry = geometry


class StationInfo:

    def __init__(self, sensor_name: str, sensor_type: str, ch_param: List[sel.ChannelParam], geolocation: Geolocation):
        self.sensor_name = sensor_name
        self.sensor_type = sensor_type
        self.ch_param = ch_param
        self.geolocation = geolocation


class StationMeasure:

    def __init__(self, timestamp: ts.Timestamp, measures: List[Measure]):
        self.timestamp = timestamp
        self.measures = measures


class MobileMeasure:

    def __init__(self, measures: List[Measure], geolocation: Geolocation):
        self.geolocation = geolocation
        self.measures = measures


# Define a Union type variable for the return type
ADPTYPE = Union[MobileMeasure, StationMeasure, StationInfo]
