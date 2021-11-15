######################################################
#
# Author: Davide Colombo
# Date: 02/11/21 12:29
# Description: this script defines a class for building geometry type string based on API parameters
#
######################################################
import abc
from typing import Dict, Any

ST_GEOM_FROM_TEXT = "ST_GeomFromText('{geom}', {srid})"
POINT_GEOMETRY = "POINT({lng} {lat})"


def get_postgis_class(sensor_type: str):

    if sensor_type == 'purpleair':
        return PointBuilder
    else:
        return None


class GeometryBuilder(abc.ABC):

    def __init__(self, packet: Dict[str, Any], srid: int = 26918):
        self.srid = srid
        self.packet = packet

    @abc.abstractmethod
    def geom_from_text(self) -> str:
        pass

    @abc.abstractmethod
    def as_text(self) -> str:
        pass


class PointBuilder(GeometryBuilder):

    def __init__(self, packet: Dict[str, Any], srid: int = 26918):
        super(PointBuilder, self).__init__(packet=packet, srid=srid)
        if 'lat' not in self.packet:
            raise SystemExit(f"{PointBuilder.__name__}: bad packet => missing key='lat'")
        elif 'lng' not in self.packet:
            raise SystemExit(f"{PointBuilder.__name__}: bad packet => missing key='lng'")

    def geom_from_text(self) -> str:
        geom = POINT_GEOMETRY.format(lng=self.packet['lng'], lat=self.packet['lat'])
        return ST_GEOM_FROM_TEXT.format(geom=geom, srid=self.srid)

    def as_text(self) -> str:
        return POINT_GEOMETRY.format(lng=self.packet['lng'], lat=self.packet['lat'])
