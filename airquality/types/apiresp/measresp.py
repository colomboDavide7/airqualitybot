######################################################
#
# Author: Davide Colombo
# Date: 26/11/21 10:43
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List
import airquality.types.timestamp as ts
import airquality.types.postgis as pgis


class ParamNameValue:

    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value


class MeasureAPIResp:

    def __init__(self, timestamp: ts.Timestamp, measures: List[ParamNameValue]):
        self.timestamp = timestamp
        self.measures = measures


################################ MOBILE SENSOR API RESPONSE ################################
class MobileSensorAPIResp(MeasureAPIResp):

    def __init__(self, timestamp: ts.Timestamp, measures: List[ParamNameValue], geometry: pgis.PostgisPoint):
        super(MobileSensorAPIResp, self).__init__(timestamp=timestamp, measures=measures)
        self.geometry = geometry
