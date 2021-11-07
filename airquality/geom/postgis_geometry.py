######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 02/11/21 12:29
# Description: this script defines a class for building geometry type string based on API parameters
#
######################################################
from typing import Dict, Any
from abc import ABC, abstractmethod


class PostGISGeometry(ABC):

    def __init__(self, param: Dict[str, Any]):
        self.param = param

    @abstractmethod
    def get_database_string(self) -> str:
        pass

    @abstractmethod
    def get_geomtype_string(self) -> str:
        pass


class PostGISPoint(PostGISGeometry):

    def __init__(self, param: Dict[str, Any]):
        super().__init__(param)
        self.lat = param.get('lat')
        self.lng = param.get('lng')

    def get_database_string(self) -> str:
        return f"ST_GeomFromText('POINT({self.lng} {self.lat})', 26918)"

    def get_geomtype_string(self) -> str:
        return f"POINT({self.lng} {self.lat})"


class PostGISNullObject(PostGISGeometry):

    def get_database_string(self):
        return None

    def get_geomtype_string(self):
        return None


################################ FACTORY ################################
class PostGISGeometryFactory:

    def __init__(self, geom_class=PostGISGeometry):
        self.geom_class = geom_class

    def create_geometry(self, param: Dict[str, Any]) -> PostGISGeometry:
        if not param:
            return PostGISNullObject(param)
        return self.geom_class(param)
