######################################################
#
# Author: Davide Colombo
# Date: 02/11/21 12:29
# Description: this script defines a class for building geometry type string based on API parameters
#
######################################################
import abc

GEOM_FROM_TEXT = "ST_GeomFromText('{geom}', {srid})"
POINT_GEOM = "POINT({lng} {lat})"


# ------------------------------- PostgisABC ------------------------------- #
class PostgisABC(abc.ABC):

    def __init__(self, srid: int = 26918):
        self.srid = srid

    @abc.abstractmethod
    def geom_from_text(self) -> str:
        pass

    @abc.abstractmethod
    def as_text(self) -> str:
        pass


# ------------------------------- PostgisPoint ------------------------------- #
class PostgisPoint(PostgisABC):

    def __init__(self, lat: str, lng: str, srid: int = 26918):
        super(PostgisPoint, self).__init__(srid=srid)
        self.lat = lat
        self.lng = lng

    def geom_from_text(self) -> str:
        geom = POINT_GEOM.format(lng=self.lng, lat=self.lat)
        return GEOM_FROM_TEXT.format(geom=geom, srid=self.srid)

    def as_text(self) -> str:
        return POINT_GEOM.format(lng=self.lng, lat=self.lat)


# ------------------------------- NullGeometry ------------------------------- #
class NullGeometry(PostgisABC):

    def __init__(self, srid: int = 26918):
        super(NullGeometry, self).__init__(srid=srid)

    def geom_from_text(self) -> str:
        return "NULL"

    def as_text(self) -> str:
        return "NULL"
