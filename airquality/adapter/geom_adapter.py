######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 06/11/21 11:23
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any
from abc import ABC, abstractmethod
from airquality.geom.postgis_geometry import PostGISNullObject, PostGISPoint, PostGISGeometry


class GeometryAdapter(ABC):

    @abstractmethod
    def adapt(self, packet: Dict[str, Any]) -> PostGISGeometry:
        pass


class GeometryAdapterPurpleair(GeometryAdapter):

    def adapt(self, packet: Dict[str, Any]) -> PostGISPoint:
        keys = packet.keys()
        if 'latitude' not in keys or 'longitude' not in keys:
            raise SystemExit(f"{GeometryAdapterPurpleair.__name__} missing required geometry fields=['latitude' | 'longitude']")
        return PostGISPoint(lat=packet.pop('latitude'), lng=packet.pop('longitude'))


class GeometryAdapterAtmotube(GeometryAdapter):

    def adapt(self, packet: Dict[str, Any]) -> PostGISGeometry:
        keys = packet.keys()
        if 'coords' not in keys:
            return PostGISNullObject()
        coords = packet.pop('coords')
        return PostGISPoint(lat=coords['lat'], lng=coords['lon'])
