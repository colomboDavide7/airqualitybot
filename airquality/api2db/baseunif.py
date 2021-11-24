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
import airquality.database.postgis.geom as geo
import airquality.database.datatype.timestamp as ts


class ParamNameTimestamp:

    def __init__(self, name: str, timestamp: ts.Timestamp):
        self.name = name
        self.timestamp = timestamp


class ParamLocationTimestamp:

    def __init__(self, timestamp: ts.Timestamp, geolocation: geo.PostgisGeometry):
        self.timestamp = timestamp
        self.geolocation = geolocation


class BaseUniformResponse(abc.ABC):
    pass


class BaseUniformResponseBuilder(abc.ABC):

    @abc.abstractmethod
    def build(self, responses: List[mdl.BaseAPIResponse]) -> List[BaseUniformResponse]:
        pass
