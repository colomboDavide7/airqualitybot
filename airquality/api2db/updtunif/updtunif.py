######################################################
#
# Author: Davide Colombo
# Date: 24/11/21 09:59
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
import airquality.api2db.baseunif as base
import airquality.database.postgis.geom as geo
import airquality.database.datatype.timestamp as ts


class UpdateUniformResponse(base.BaseUniformResponse):

    def __init__(self, geolocation: base.ParamLocationTimestamp):
        self.geolocation = geolocation


class UpdateUniformResponseBuilder(base.BaseUniformResponseBuilder, abc.ABC):

    def __init__(self, timestamp_class=ts.Timestamp, postgis_class=geo.PostgisPoint):
        self.timestamp_class = timestamp_class
        self.postgis_class = postgis_class
