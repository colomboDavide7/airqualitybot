######################################################
#
# Author: Davide Colombo
# Date: 24/11/21 09:59
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import List
import airquality.api2db.baseunif as base
import airquality.database.ext.postgis as geo
import airquality.database.dtype.timestamp as ts


class UpdateUniformResponse(base.BaseUniformResponse):

    def __init__(self, sensor_name: str, geolocation: base.ParamLocationTimestamp):
        self.geolocation = geolocation
        self.sensor_name = sensor_name


class UpdateUniformResponseBuilder(base.BaseUniformResponseBuilder, abc.ABC):

    def __init__(self, timestamp_class=ts.UnixTimestamp, postgis_class=geo.PostgisPoint):
        self.timestamp_class = timestamp_class
        self.postgis_class = postgis_class

    @abc.abstractmethod
    def uniform(self, responses: List[base.mdl.BaseResponse]) -> List[UpdateUniformResponse]:
        pass
