######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 20:08
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import List
import airquality.api.model.baseresp as basemdl
import airquality.adapter.api2db.baseadpt as base
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


################################ INIT UNIFORM MODEL ################################
class InitUniformModel(base.BaseUniformModel):

    def __init__(self, name: str, type_: str,
                 parameters: List[basemdl.ParamNameValue],
                 channels: List[ParamNameTimestamp],
                 geolocation: ParamLocationTimestamp
    ):
        self.name = name
        self.type = type_
        self.parameters = parameters
        self.channels = channels
        self.geolocation = geolocation


################################ INIT API 2 DB ADAPTER ################################
class InitAPI2DBAdapter(base.BaseAPI2DBAdapter, abc.ABC):

    def __init__(self, timestamp_class=ts.Timestamp, postgis_class=geo.PostgisPoint):
        self.timestamp_class = timestamp_class
        self.postgis_class = postgis_class
