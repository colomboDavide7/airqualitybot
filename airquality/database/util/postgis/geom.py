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

    if sensor_type in ('purpleair', 'atmotube'):
        return PointBuilder
    else:
        return None


class GeometryBuilder(abc.ABC):

    def __init__(self, srid: int = 26918):
        self.srid = srid

    @abc.abstractmethod
    def geom_from_text(self, sensor_data: Dict[str, Any]) -> str:
        pass

    @abc.abstractmethod
    def as_text(self, sensor_data: Dict[str, Any]) -> str:
        pass

    @abc.abstractmethod
    def _exit_on_missing_arguments(self, sensor_data: Dict[str, Any]):
        pass


class PointBuilder(GeometryBuilder):

    def __init__(self, srid: int = 26918):
        super(PointBuilder, self).__init__(srid=srid)

    def geom_from_text(self, sensor_data: Dict[str, Any]) -> str:
        self._exit_on_missing_arguments(sensor_data)
        geom = POINT_GEOMETRY.format(lng=sensor_data['lng'], lat=sensor_data['lat'])
        return ST_GEOM_FROM_TEXT.format(geom=geom, srid=self.srid)

    def as_text(self, sensor_data: Dict[str, Any]) -> str:
        self._exit_on_missing_arguments(sensor_data)
        return POINT_GEOMETRY.format(lng=sensor_data['lng'], lat=sensor_data['lat'])

    def _exit_on_missing_arguments(self, sensor_data: Dict[str, Any]):
        if 'lat' not in sensor_data:
            raise SystemExit(f"{PointBuilder.__name__}: bad packet => missing key='lat'")
        elif 'lng' not in sensor_data:
            raise SystemExit(f"{PointBuilder.__name__}: bad packet => missing key='lng'")
