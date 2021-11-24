######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 20:08
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import List
import airquality.api.resp.baseresp as baseresp
import airquality.api2db.baseunif as baseunif
import airquality.database.ext.postgis as postgis
import airquality.database.dtype.timestamp as ts


################################ INIT UNIFORM MODEL ################################
class InitUniformResponse(baseunif.BaseUniformResponse):

    def __init__(
            self, name: str, type_: str,
            parameters: List[baseresp.ParamNameValue],
            channels: List[baseunif.ParamNameTimestamp],
            geolocation: baseunif.ParamLocationTimestamp
    ):
        self.name = name
        self.type = type_
        self.parameters = parameters
        self.channels = channels
        self.geolocation = geolocation


################################ INIT API 2 DB ADAPTER ################################
class InitUniformResponseBuilder(baseunif.BaseUniformResponseBuilder, abc.ABC):

    def __init__(self, timestamp_class=ts.UnixTimestamp, postgis_class=postgis.PostgisPoint):
        self.timestamp_class = timestamp_class
        self.postgis_class = postgis_class

    @abc.abstractmethod
    def uniform(self, responses: List[baseresp.BaseResponse]) -> List[InitUniformResponse]:
        pass
