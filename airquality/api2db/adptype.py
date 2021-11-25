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


class ChannelParam:

    def __init__(self, ch_id: str, ch_key: str, ch_name: str, last_acquisition: ts.SQLTimestamp):
        self.ch_id = ch_id
        self.ch_key = ch_key
        self.ch_name = ch_name
        self.last_acquisition = last_acquisition


class ParamIDName:

    def __init__(self, id_: int, value: str):
        self.param_id = id_
        self.param_val = value


class Geolocation:

    def __init__(self, timestamp: ts.Timestamp, geometry: pgis.PostgisGeometry):
        self.timestamp = timestamp
        self.geometry = geometry


class StationInfo:

    def __init__(self, sensor_name: str, sensor_type: str, ch_param: List[ChannelParam], geolocation: Geolocation):
        self.sensor_name = sensor_name
        self.sensor_type = sensor_type
        self.ch_param = ch_param
        self.geolocation = geolocation


class Measure:

    def __init__(self, measures: List[ParamIDName], timestamp: ts.Timestamp):
        self.measures = measures
        self.timestamp = timestamp


class StationMeasure(Measure):

    def __init__(self, timestamp: ts.Timestamp, measures: List[ParamIDName]):
        super(StationMeasure, self).__init__(timestamp=timestamp, measures=measures)


class MobileMeasure(Measure):

    def __init__(self, measures: List[ParamIDName], timestamp: ts.Timestamp, geometry: pgis.PostgisGeometry):
        super(MobileMeasure, self).__init__(measures=measures, timestamp=timestamp)
        self.geometry = geometry


# Define a Union type variable for the return type
ADPTYPE = Union[MobileMeasure, StationMeasure, StationInfo]
