######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 20:08
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import List
import airquality.api.resp.baseresp as basemdl
import airquality.api2db.baseunif as base
import airquality.database.ext.postgis as geo
import airquality.database.dtype.timestamp as ts


################################ INIT UNIFORM MODEL ################################
class InitUniformResponse(base.BaseUniformResponse):

    def __init__(
            self, name: str, type_: str,
            parameters: List[basemdl.ParamNameValue],
            channels: List[base.ParamNameTimestamp],
            geolocation: base.ParamLocationTimestamp
    ):
        self.name = name
        self.type = type_
        self.parameters = parameters
        self.channels = channels
        self.geolocation = geolocation


################################ INIT API 2 DB ADAPTER ################################
class InitUniformResponseBuilder(base.BaseUniformResponseBuilder, abc.ABC):

    def __init__(self, timestamp_class=ts.UnixTimestamp, postgis_class=geo.PostgisPoint):
        self.timestamp_class = timestamp_class
        self.postgis_class = postgis_class

    @abc.abstractmethod
    def build(self, responses: List[basemdl.BaseAPIResponse]) -> List[InitUniformResponse]:
        pass
