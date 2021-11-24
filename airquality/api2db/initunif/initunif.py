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
import airquality.database.op.sel.sel as sel


################################ INIT UNIFORM MODEL ################################
class InitUniformResponse(baseunif.BaseUniformResponse):

    def __init__(
            self,
            name: str,
            type_: str,
            channel_param: List[sel.ChannelParam],
            geolocation: baseunif.ParamLocationTimestamp
    ):
        self.name = name
        self.type = type_
        self.channel_param = channel_param
        self.geolocation = geolocation


################################ INIT API 2 DB ADAPTER ################################
class InitUniformResponseBuilder(baseunif.BaseUniformResponseBuilder, abc.ABC):

    def __init__(self, timestamp_class=ts.UnixTimestamp, postgis_class=postgis.PostgisPoint):
        self.timestamp_class = timestamp_class
        self.postgis_class = postgis_class

    @abc.abstractmethod
    def uniform(self, responses: List[baseresp.BaseResponse]) -> List[InitUniformResponse]:
        pass
