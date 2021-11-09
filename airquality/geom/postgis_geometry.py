######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 02/11/21 12:29
# Description: this script defines a class for building geometry type string based on API parameters
#
######################################################
from abc import ABC, abstractmethod
from airquality.constants.shared_constants import EXCEPTION_HEADER


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
        return f"ST_GeomFromText('POINT({self.lng} {self.lat})', 26918)"

    def get_geomtype_string(self) -> str:
        return f"POINT({self.lng} {self.lat})"

    def __eq__(self, other):
        if not isinstance(other, PostGISPoint):
            raise SystemExit(f"{EXCEPTION_HEADER} {PostGISPoint.__name__} cannot be compared with object of type => "
                             f"'{other.__class__.__name__}'.")
        return self.lat == other.lat and self.lng == other.lng


############################## NULL OBJECT USED WHEN COORDS ARE MISSING #############################
class PostGISNullObject(PostGISGeometry):

    def get_database_string(self):
        return 'null'

    def get_geomtype_string(self):
        return 'null'

    def __eq__(self, other):
        if not isinstance(other, PostGISNullObject):
            raise SystemExit(f"{EXCEPTION_HEADER} {PostGISNullObject.__name__} cannot be compared with object of type => "
                             f"'{other.__class__.__name__}'.")
        return True
