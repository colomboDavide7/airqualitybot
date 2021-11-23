######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 17:06
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import List, Dict, Any
import airquality.adapter.api2db.baseadpt as base
import airquality.database.util.datatype.timestamp as ts
import airquality.database.util.postgis.geom as geo


class ParamIDValue:

    def __init__(self, id_: int, value: str):
        self.id = id_
        self.value = value


class FetchUniformModel(base.BaseUniformModel):

    def __init__(self, timestamp: ts.Timestamp, parameters: List[ParamIDValue], geolocation=geo.NullGeometry()):
        self.timestamp = timestamp
        self.parameters = parameters
        self.geolocation = geolocation


################################ FETCH ADAPTER BASE CLASS ###############################
class FetchAPI2DBAdapter(base.BaseAPI2DBAdapter, abc.ABC):

    def __init__(self, measure_param_map: Dict[str, Any], timestamp_class=ts.Timestamp):
        self.measure_param_map = measure_param_map
        self.timestamp_class = timestamp_class
