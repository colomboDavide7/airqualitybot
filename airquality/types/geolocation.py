######################################################
#
# Author: Davide Colombo
# Date: 26/11/21 10:19
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import types.postgis as pgis
import airquality.types.timestamp as ts


class Geolocation:

    def __init__(self, timestamp: ts.Timestamp, geometry: pgis.PostgisGeometry):
        self.timestamp = timestamp
        self.geometry = geometry
