######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 04/11/21 08:28
# Description: Plain object that represents the API parameters corresponding to a sensor selected from the database
#
######################################################
import builtins
from typing import Dict, Any
from airquality.constants.shared_constants import PARAM_DEFAULT_VALUE


class PlainAPIParamThingspeak(builtins.object):

    def __init__(self, api_param: Dict[str, Any]):
        self.primary_id_a = api_param.get('primary_id_a', PARAM_DEFAULT_VALUE)
        self.primary_key_a = api_param.get('primary_key_a', PARAM_DEFAULT_VALUE)
        self.primary_id_b = api_param.get('primary_id_b', PARAM_DEFAULT_VALUE)
        self.primary_key_b = api_param.get('primary_key_b', PARAM_DEFAULT_VALUE)
        self.secondary_id_a = api_param.get('secondary_id_a', PARAM_DEFAULT_VALUE)
        self.secondary_key_a = api_param.get('secondary_key_a', PARAM_DEFAULT_VALUE)
        self.secondary_id_b = api_param.get('secondary_id_b', PARAM_DEFAULT_VALUE)
        self.secondary_key_b = api_param.get('secondary_key_b', PARAM_DEFAULT_VALUE)
        self.primary_timestamp_a = api_param.get('primary_timestamp_a', None)
        self.primary_timestamp_b = api_param.get('primary_timestamp_b', None)
        self.secondary_timestamp_a = api_param.get('secondary_timestamp_a', None)
        self.secondary_timestamp_b = api_param.get('secondary_timestamp_b', None)

    def __str__(self):
        return f"primary_id_a={self.primary_id_a}, primary_key_a={self.primary_key_a}, " \
               f"primary_id_b={self.primary_id_b}, primary_key_b={self.primary_key_b}, " \
               f"secondary_id_a={self.secondary_id_a}, secondary_key_a={self.secondary_key_a}, " \
               f"secondary_id_b={self.secondary_id_b}, secondary_key_b={self.secondary_key_b}, " \
               f"primary_timestamp_a={self.primary_timestamp_a}, primary_timestamp_b={self.primary_timestamp_b}, " \
               f"secondary_timestamp_a={self.secondary_timestamp_a}, secondary_timestamp_b={self.secondary_timestamp_b}"
