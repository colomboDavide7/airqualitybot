######################################################
#
# Author: Davide Colombo
# Date: 06/12/21 19:10
# Description: INSERT HERE THE DESCRIPTION
#
######################################################

################################ DATABASE LOOKUP ABC ###############################
import abc


class DatabaseLookupABC(abc.ABC):
    pass


################################ SENSOR INFO LOOKUP ###############################
import airquality.types.postgis as pgistype


class SensorInfoLookup(DatabaseLookupABC):

    def __init__(self, sensor_name: str):
        self.sensor_name = sensor_name


################################ SENSOR GEO LOOKUP ###############################
class SensorGeoLookup(DatabaseLookupABC):

    def __init__(self, sensor_name: str, geometry: pgistype.PostgisGeometry):
        self.sensor_name = sensor_name
        self.geometry = geometry


################################ SENSOR MEASURE LOOKUP ###############################
from typing import List
import airquality.types.channel as chtype


class SensorMeasureLookup(DatabaseLookupABC):

    def __init__(self, sensor_id: int, channels: List[chtype.Channel]):
        self.sensor_id = sensor_id
        self.channels = channels


################################ SENSOR MEASURE LOOKUP ###############################
class GeoAreaLookup(DatabaseLookupABC):

    def __init__(
            self, postal_code: str, place_name: str, country_code: str, state: str, province: str, geom: pgistype.PostgisGeometry
    ):
        self.postal_code = postal_code
        self.place_name = place_name
        self.country_code = country_code
        self.state = state
        self.province = province
        self.geom = geom
