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
        return PostGISPoint(lat=packet['lat'], lng=packet['lng'])


class GeometryAdapterAtmotube(GeometryAdapter):

    def adapt(self, packet: Dict[str, Any]) -> PostGISGeometry:
        if 'coords' not in packet.keys():
            return PostGISNullObject()
        coords = packet.pop('coords')
        return PostGISPoint(lat=coords['lat'], lng=coords['lon'])
