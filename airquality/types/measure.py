######################################################
#
# Author: Davide Colombo
# Date: 26/11/21 10:21
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List
import types.postgis as pgis
import airquality.types.timestamp as ts


class ParamIDValue:

    def __init__(self, id_: int, value: str):
        self.param_id = id_
        self.param_val = value


################################ MEASURE DATA TYPE ################################
class Measure:

    def __init__(self, measures: List[ParamIDValue], timestamp: ts.Timestamp):
        self.measures = measures
        self.timestamp = timestamp


class StationMeasure(Measure):

    def __init__(self, timestamp: ts.Timestamp, measures: List[ParamIDValue]):
        super(StationMeasure, self).__init__(timestamp=timestamp, measures=measures)


class MobileMeasure(Measure):

    def __init__(self, measures: List[ParamIDValue], timestamp: ts.Timestamp, geometry: pgis.PostgisGeometry):
        super(MobileMeasure, self).__init__(measures=measures, timestamp=timestamp)
        self.geometry = geometry
