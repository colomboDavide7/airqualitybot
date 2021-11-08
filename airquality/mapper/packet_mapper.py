######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 08/11/21 10:16
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any
from abc import ABC, abstractmethod
from airquality.constants.shared_constants import EXCEPTION_HEADER
from airquality.geom.postgis_geometry import PostGISPoint


class PacketMapper(ABC):

    @abstractmethod
    def reshape(self, packet: Dict[str, Any]) -> Dict[str, Any]:
        pass


class PacketMapperPurpleair(PacketMapper):
    """ name:geom mapper """

    def reshape(self, packet: Dict[str, Any]) -> Dict[str, Any]:
        keys = packet.keys()
        if 'name' not in keys or 'sensor_index' not in keys:
            raise SystemExit(f"{EXCEPTION_HEADER} {PacketMapperPurpleair.__name__} missing ['name'|'sensor_index']")
        if 'latitude' not in keys or 'longitude' not in keys:
            raise SystemExit(f"{EXCEPTION_HEADER}{PacketMapperPurpleair.__name__} missing ['latitude'|'longitude']")

        name = f"{packet['name']} ({packet['sensor_index']})"
        geometry = PostGISPoint(lat=packet['latitude'], lng=packet['longitude'])
        geom = geometry.get_geomtype_string()
        return {name: geom}
