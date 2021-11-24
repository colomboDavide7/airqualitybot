######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 17:07
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import List
import airquality.api.resp.baseresp as mdl
import airquality.database.ext.postgis as geo
import airquality.database.dtype.timestamp as ts


class ParamNameTimestamp:

    def __init__(self, name: str, timestamp: ts.Timestamp):
        self.name = name
        self.timestamp = timestamp


class ParamLocationTimestamp:

    def __init__(self, timestamp: ts.Timestamp, geometry: geo.PostgisGeometry):
        self.timestamp = timestamp
        self.geometry = geometry


class BaseUniformResponse(abc.ABC):
    pass


class BaseUniformResponseBuilder(abc.ABC):

    @abc.abstractmethod
    def uniform(self, responses: List[mdl.BaseResponse]) -> List[BaseUniformResponse]:
        pass
