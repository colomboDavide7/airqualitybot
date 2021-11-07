######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 06/11/21 09:19
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any
from abc import ABC, abstractmethod
from airquality.constants.shared_constants import EXCEPTION_HEADER


class ContainerAdapter(ABC):

    @abstractmethod
    def adapt_packet(self, packet: Dict[str, Any]) -> Dict[str, Any]:
        pass


class ContainerAdapterPurpleair(ContainerAdapter):

    def adapt_packet(self, packet: Dict[str, Any]) -> Dict[str, Any]:
        new_packet = {}
        try:
            new_packet['name'] = f"{packet['name']} ({packet['sensor_index']})"
            new_packet['type'] = 'purpleair'
            new_packet['timestamp'] = packet['timestamp']
            new_packet['geometry'] = packet['geometry']
            new_packet['param_name'] = ['primary_id_a',
                                        'primary_id_b',
                                        'primary_key_a',
                                        'primary_key_b',
                                        'secondary_id_a',
                                        'secondary_id_b',
                                        'secondary_key_a',
                                        'secondary_key_b',
                                        'primary_timestamp_a',
                                        'primary_timestamp_b',
                                        'secondary_timestamp_a',
                                        'secondary_timestamp_b']
            new_packet['param_value'] = [packet['primary_id_a'],
                                         packet['primary_id_b'],
                                         packet['primary_key_a'],
                                         packet['primary_key_b'],
                                         packet['secondary_id_a'],
                                         packet['secondary_id_b'],
                                         packet['secondary_key_a'],
                                         packet['secondary_key_b'],
                                         '2018-01-01 00:00:00',
                                         '2018-01-01 00:00:00',
                                         '2018-01-01 00:00:00',
                                         '2018-01-01 00:00:00']
        except KeyError as ke:
            # Raise Exception if any key is missing from the 'packet' dictionary
            raise SystemExit(f"{EXCEPTION_HEADER} {ContainerAdapterPurpleair.__name__} is missing the key={ke!s}.")
        return new_packet


################################ CONTAINER ADAPTER FACTORY ################################
class ContainerAdapterFactory(object):

    def __init__(self, container_adapter_class=ContainerAdapter):
        self.container_adapter_class = container_adapter_class

    def make_container_adapter(self) -> ContainerAdapter:
        return self.container_adapter_class()
