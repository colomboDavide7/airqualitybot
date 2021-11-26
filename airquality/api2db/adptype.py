######################################################
#
# Author: Davide Colombo
# Date: 25/11/21 12:02
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List, Union
import types.postgis as pgis
import airquality.types.timestamp as ts
import airquality.types.geolocation as geotype
import airquality.types.channel as chtype


################################ INFO RESPONSE ADAPTER ################################
class StationInfo:

    def __init__(self, sensor_name: str, sensor_type: str, ch_param: List[chtype.Channel], geolocation: geotype.Geolocation):
        self.sensor_name = sensor_name
        self.sensor_type = sensor_type
        self.ch_param = ch_param
        self.geolocation = geolocation


################################ MEASURE RESPONSE ADAPTER ################################
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
