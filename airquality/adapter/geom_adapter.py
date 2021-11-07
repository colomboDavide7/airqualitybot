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


class GeometryAdapter(ABC):

    @abstractmethod
    def adapt_packet(self, packet: Dict[str, Any]) -> Dict[str, Any]:
        pass


class GeometryAdapterPurpleair(GeometryAdapter):

    def adapt_packet(self, packet: Dict[str, Any]) -> Dict[str, Any]:
        keys = packet.keys()
        if 'latitude' not in keys or 'longitude' not in keys:
            raise SystemExit(f"{GeometryAdapterPurpleair.__name__} missing required geometry "
                             f"fields=['latitude' | 'longitude']")
        return {'lat': packet.pop('latitude'), 'lng': packet.pop('longitude')}


class GeometryAdapterAtmotube(GeometryAdapter):

    def adapt_packet(self, packet: Dict[str, Any]) -> Dict[str, Any]:
        keys = packet.keys()
        if 'coords' not in keys:
            return {}
        coords = packet.pop('coords')
        return {'lat': coords['lat'], 'lng': coords['lon']}


class GeometryAdapterFactory:

    def __init__(self, geom_adapter_class=GeometryAdapter):
        self.geom_adapter_class = geom_adapter_class

    def make_geometry_adapter(self) -> GeometryAdapter:
        return self.geom_adapter_class()
