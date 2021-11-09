######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 02/11/21 12:29
# Description: this script defines a class for building geometry type string based on API parameters
#
######################################################
import abc
from typing import Dict, Any
from airquality.core.constants.shared_constants import EXCEPTION_HEADER

ST_GEOM_FROM_TEXT = "ST_GeomFromText('{geom}', {srid})"
POINT_GEOMETRY = "POINT({lng} {lat})"


class GeometryBuilder(abc.ABC):

    def __init__(self, srid: int):
        self.srid = srid

    @abc.abstractmethod
    def geom_from_text(self) -> str:
        pass

    @abc.abstractmethod
    def as_text(self) -> str:
        pass


class PointBuilder(GeometryBuilder):

    def __init__(self, srid: int, packet: Dict[str, Any]):
        super().__init__(srid)
        try:
            self.lat = packet['lat']
            self.lng = packet['lng']
        except KeyError as ke:
            raise SystemExit(f"{EXCEPTION_HEADER} {PointBuilder.__name__} missing required key={ke!s}")

    def geom_from_text(self) -> str:
        geom = POINT_GEOMETRY.format(lng=self.lng, lat=self.lat)
        return ST_GEOM_FROM_TEXT.format(geom=geom, srid=self.srid)

    def as_text(self) -> str:
        return POINT_GEOMETRY.format(lng=self.lng, lat=self.lat)
