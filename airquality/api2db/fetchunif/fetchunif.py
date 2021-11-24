######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 17:06
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import List, Dict, Any
import airquality.api2db.baseunif as baseadpt
import airquality.api.resp.baseresp as basersp
import airquality.database.dtype.timestamp as ts
import airquality.database.ext.postgis as geo


class ParamIDValue:

    def __init__(self, id_: int, value: str):
        self.id = id_
        self.value = value


class FetchUniformResponse(baseadpt.BaseUniformResponse):

    def __init__(self, timestamp: ts.Timestamp, parameters: List[ParamIDValue], geolocation=geo.NullGeometry()):
        self.timestamp = timestamp
        self.parameters = parameters
        self.geolocation = geolocation


################################ FETCH ADAPTER BASE CLASS ###############################
class FetchUniformResponseBuilder(baseadpt.BaseUniformResponseBuilder, abc.ABC):

    def __init__(self, measure_param_map: Dict[str, Any], timestamp_class=ts.Timestamp):
        self.measure_param_map = measure_param_map
        self.timestamp_class = timestamp_class

    @abc.abstractmethod
    def uniform(self, responses: List[basersp.BaseResponse]) -> List[FetchUniformResponse]:
        pass
