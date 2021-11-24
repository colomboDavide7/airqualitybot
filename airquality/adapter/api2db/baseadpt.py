######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 17:07
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import List
import airquality.api.model.baseresp as mdl
import airquality.database.util.postgis.geom as geo
import airquality.database.util.datatype.timestamp as ts


class ParamNameTimestamp:

    def __init__(self, name: str, timestamp: ts.Timestamp):
        self.name = name
        self.timestamp = timestamp


class ParamLocationTimestamp:

    def __init__(self, timestamp: ts.Timestamp, geolocation: geo.PostgisGeometry):
        self.timestamp = timestamp
        self.geolocation = geolocation


class BaseUniformModel(abc.ABC):
    pass


class BaseAPI2DBAdapter(abc.ABC):

    @abc.abstractmethod
    def adapt(self, responses: List[mdl.BaseResponseModel]) -> List[BaseUniformModel]:
        pass
