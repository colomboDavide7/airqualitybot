######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 02/11/21 12:29
# Description: this script defines a class for building geometry type string based on API parameters
#
######################################################
from abc import ABC, abstractmethod


class PostGISGeometry(ABC):

    @abstractmethod
    def get_database_string(self) -> str:
        pass

    @abstractmethod
    def get_geomtype_string(self) -> str:
        pass


class PostGISPoint(PostGISGeometry):

    def __init__(self, lat: str, lng: str):
        self.lat = lat
        self.lng = lng

    def get_database_string(self) -> str:
        return f"ST_GeomFromText('POINT({self.lng} {self.lat})')"

    def get_geomtype_string(self) -> str:
        return f"POINT({self.lng} {self.lat})"


################################ FACTORY ################################
class PostGISGeometryFactory(ABC):

    @abstractmethod
    def create_geometry(self) -> PostGISGeometry:
        pass


class PostGISPointFactory(PostGISGeometryFactory):

    def __init__(self, lat: str, lng: str):
        self.lat = lat
        self.lng = lng

    def create_geometry(self) -> PostGISGeometry:
        return PostGISPoint(lat=self.lat, lng=self.lng)
