######################################################
#
# Author: Davide Colombo
# Date: 22/11/21 19:29
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.database.util.datatype.timestamp as ts
import airquality.database.util.postgis.geom as geo


class LocationContainer:

    def __init__(self, valid_from: ts.Timestamp, postgis_geom: geo.PostgisGeometry):
        self.valid_from = valid_from
        self.postgis_geom = postgis_geom
