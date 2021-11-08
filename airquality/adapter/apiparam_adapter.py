######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 08/11/21 08:55
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any
from abc import ABC, abstractmethod
from airquality.container.sql_container import APIParamSQLContainer
from airquality.constants.shared_constants import EXCEPTION_HEADER


class APIParamAdapter(ABC):

    @abstractmethod
    def adapt(self, sensor_id: int, packet: Dict[str, Any]) -> APIParamSQLContainer:
        pass


class APIParamAdapterPurpleair(APIParamAdapter):

    def adapt(self, sensor_id: int, packet: Dict[str, Any]) -> APIParamSQLContainer:
        keys = packet.keys()
        if 'primary_id_a' not in keys or 'primary_key_a' not in keys:
            raise SystemExit(f"{EXCEPTION_HEADER} {APIParamAdapterPurpleair.__name__} missing ['primary_id_a'|'primary_key_a']")
        if 'primary_id_b' not in keys or 'primary_key_b' not in keys:
            raise SystemExit(f"{EXCEPTION_HEADER} {APIParamAdapterPurpleair.__name__} missing ['primary_id_b'|'primary_key_b']")
        if 'secondary_id_a' not in keys or 'secondary_key_a' not in keys:
            raise SystemExit(f"{EXCEPTION_HEADER} {APIParamAdapterPurpleair.__name__} missing ['secondary_id_a'|'secondary_key_a']")
        if 'secondary_id_b' not in keys or 'secondary_key_b' not in keys:
            raise SystemExit(f"{EXCEPTION_HEADER} {APIParamAdapterPurpleair.__name__} missing ['secondary_id_b'|'secondary_key_b']")

        param_name = ['primary_id_a', 'primary_key_a', 'primary_id_b', 'primary_key_b',
                      'secondary_id_a', 'secondary_key_a', 'secondary_id_b', 'secondary_key_b']
        param_value = [packet['primary_id_a'], packet['primary_key_a'], packet['primary_id_b'], packet['primary_key_b'],
                       packet['secondary_id_a'], packet['secondary_key_a'], packet['secondary_id_b'], packet['secondary_key_b']]

        return APIParamSQLContainer(sensor_id=sensor_id, param_name=param_name, param_value=param_value)
