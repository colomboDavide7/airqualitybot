######################################################
#
# Author: Davide Colombo
# Date: 02/11/21 12:29
# Description: this script defines a class for building geometry type string based on API parameters
#
######################################################
import abc

ST_GEOM_FROM_TEXT = "ST_GeomFromText('{geom}', {srid})"
POINT_GEOMETRY = "POINT({lng} {lat})"


def get_postgis_class(sensor_type: str):

    if sensor_type in ('purpleair', 'atmotube'):
        return PostgisPoint
    else:
        return None


################################ GEOMETRY BUILDER CLASS ################################
class PostgisGeometry(abc.ABC):

    def __init__(self, srid: int = 26918):
        self.srid = srid

    @abc.abstractmethod
    def geom_from_text(self) -> str:
        pass

    @abc.abstractmethod
    def as_text(self) -> str:
        pass


################################ POINT BUILDER CLASS ################################
class PostgisPoint(PostgisGeometry):

    def __init__(self, lat: str, lng: str, srid: int = 26918):
        super(PostgisPoint, self).__init__(srid=srid)
        self.lat = lat
        self.lng = lng

    def geom_from_text(self) -> str:
        geom = POINT_GEOMETRY.format(lng=self.lng, lat=self.lat)
        return ST_GEOM_FROM_TEXT.format(geom=geom, srid=self.srid)

    def as_text(self) -> str:
        return POINT_GEOMETRY.format(lng=self.lng, lat=self.lat)


################################ NULL GEOMETRY CLASS ################################
class NullGeometry(PostgisGeometry):

    def __init__(self, srid: int = 26918):
        super(NullGeometry, self).__init__(srid=srid)

    def geom_from_text(self) -> str:
        return "NULL"

    def as_text(self) -> str:
        return "NULL"
