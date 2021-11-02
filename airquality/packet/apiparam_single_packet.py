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


class APIParamSinglePacket(ABC):
    pass


class APIParamSinglePacketPurpleair(APIParamSinglePacket):

    def __init__(self, api_param: Dict[str, Any]):
        self.name = api_param['name']
        self.sensor_index = api_param['sensor_index']
        self.latitude = api_param['latitude']
        self.longitude = api_param['longitude']
        self.primary_id_a = api_param['primary_id_a']
        self.primary_key_a = api_param['primary_key_a']
        self.primary_id_b = api_param['primary_id_b']
        self.primary_key_b = api_param['primary_key_b']
        self.secondary_id_a = api_param['secondary_id_a']
        self.secondary_key_a = api_param['secondary_key_a']
        self.secondary_id_b = api_param['secondary_id_b']
        self.secondary_key_b = api_param['secondary_key_b']
        self.purpleair_identifier = f"{self.name} ({self.sensor_index})"

    def __str__(self):
        return f"name={self.name}, sensor_index={self.sensor_index}, identifier={self.purpleair_identifier}, " \
               f"latitude={self.latitude}, longitude={self.longitude}, " \
               f"primary_id_a={self.primary_id_a}, primary_key_a={self.primary_key_a}, " \
               f"primary_id_b={self.primary_id_b}, primary_key_b={self.primary_key_b}, " \
               f"secondary_id_a={self.secondary_id_a}, secondary_key_a={self.secondary_key_a}, " \
               f"secondary_id_b={self.secondary_id_b}, secondary_key_b={self.secondary_key_b}"
