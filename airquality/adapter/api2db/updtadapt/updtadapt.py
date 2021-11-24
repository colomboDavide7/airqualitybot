######################################################
#
# Author: Davide Colombo
# Date: 24/11/21 09:59
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
import airquality.adapter.api2db.baseadpt as base
import airquality.database.util.postgis.geom as geo
import airquality.database.util.datatype.timestamp as ts


class UpdateUniformModel(base.BaseUniformModel):

    def __init__(self, geolocation: base.ParamLocationTimestamp):
        self.geolocation = geolocation


class UpdateAPI2DBAdapter(base.BaseAPI2DBAdapter, abc.ABC):

    def __init__(self, timestamp_class=ts.Timestamp, postgis_class=geo.PostgisPoint):
        self.timestamp_class = timestamp_class
        self.postgis_class = postgis_class
