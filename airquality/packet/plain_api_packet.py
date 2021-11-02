######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 02/11/21 16:59
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from abc import ABC
from typing import Dict, Any

DEFAULT_VALUE = 'null'


class PlainAPIPacket(ABC):
    pass


class PlainAPIPacketPurpleair(PlainAPIPacket):

    def __init__(self, api_param: Dict[str, Any]):
        self.name = api_param.get('name', DEFAULT_VALUE)
        self.sensor_index = api_param.get('sensor_index', DEFAULT_VALUE)
        self.latitude = api_param.get('latitude', DEFAULT_VALUE)
        self.longitude = api_param.get('longitude', DEFAULT_VALUE)
        self.primary_id_a = api_param.get('primary_id_a', DEFAULT_VALUE)
        self.primary_key_a = api_param.get('primary_key_a', DEFAULT_VALUE)
        self.primary_id_b = api_param.get('primary_id_b', DEFAULT_VALUE)
        self.primary_key_b = api_param.get('primary_key_b', DEFAULT_VALUE)
        self.secondary_id_a = api_param.get('secondary_id_a', DEFAULT_VALUE)
        self.secondary_key_a = api_param.get('secondary_key_a', DEFAULT_VALUE)
        self.secondary_id_b = api_param.get('secondary_id_b', DEFAULT_VALUE)
        self.secondary_key_b = api_param.get('secondary_key_b', DEFAULT_VALUE)
        self.purpleair_identifier = f"{self.name} ({self.sensor_index})"

    def __str__(self):
        return f"name={self.name}, sensor_index={self.sensor_index}, identifier={self.purpleair_identifier}, " \
               f"latitude={self.latitude}, longitude={self.longitude}, " \
               f"primary_id_a={self.primary_id_a}, primary_key_a={self.primary_key_a}, " \
               f"primary_id_b={self.primary_id_b}, primary_key_b={self.primary_key_b}, " \
               f"secondary_id_a={self.secondary_id_a}, secondary_key_a={self.secondary_key_a}, " \
               f"secondary_id_b={self.secondary_id_b}, secondary_key_b={self.secondary_key_b}"

    def __eq__(self, other):
        if not isinstance(other, PlainAPIPacketPurpleair):
            raise SystemExit(f"{PlainAPIPacketPurpleair.__name__}: cannot compare objects of different type.")
        return other.purpleair_identifier == self.purpleair_identifier
