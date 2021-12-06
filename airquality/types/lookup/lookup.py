######################################################
#
# Author: Davide Colombo
# Date: 06/12/21 19:10
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc


class DatabaseLookup(abc.ABC):
    pass


import airquality.types.postgis as pgistype


class SensorInfoLookup(DatabaseLookup):

    def __init__(self, sensor_name: str):
        self.sensor_name = sensor_name


class SensorGeoLookup(DatabaseLookup):

    def __init__(self, sensor_name: str, geometry: pgistype.PostgisGeometry):
        self.sensor_name = sensor_name
        self.geometry = geometry
