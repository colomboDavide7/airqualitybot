######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 05/11/21 11:04
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from dataclasses import dataclass
from abc import ABC, abstractmethod
from airquality.parser.datetime_parser import DatetimeParser
from airquality.geom.postgis_geometry import PostGISPointFactory

# STORES SENSOR IN 'SENSOR_AT_LOCATION' TABLE


@dataclass
class GeolocationContainer(ABC):
    sensor_id: int

    @abstractmethod
    def container2sql(self) -> str:
        pass


@dataclass
class PurpleairGeolocationContainer(GeolocationContainer):
    latitude: str
    longitude: str

    def container2sql(self) -> str:
        point = PostGISPointFactory(lat=self.latitude, lng=self.longitude).create_geometry()
        ts = DatetimeParser.current_sqltimestamp()
        return f"({self.sensor_id}, '{ts}', {point.get_database_string()})"
