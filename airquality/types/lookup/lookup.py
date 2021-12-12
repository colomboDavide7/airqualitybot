######################################################
#
# Author: Davide Colombo
# Date: 06/12/21 19:10
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.types.postgis as pgistype


################################ SENSOR GEO LOOKUP ###############################
class SensorGeoLookup(object):

    def __init__(self, sensor_name: str, geometry: pgistype.PostgisGeometry):
        self.sensor_name = sensor_name
        self.geometry = geometry


################################ SENSOR MEASURE LOOKUP ###############################
class GeoareaLookup(object):

    def __init__(
            self, postal_code: str, place_name: str, country_code: str, state: str, province: str, geom: pgistype.PostgisGeometry
    ):
        self.postal_code = postal_code
        self.place_name = place_name
        self.country_code = country_code
        self.state = state
        self.province = province
        self.geom = geom
