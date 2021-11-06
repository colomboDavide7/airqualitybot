######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 06/11/21 09:19
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any, List
from abc import ABC, abstractmethod


class ContainerAdapter(ABC):

    def __init__(self, packets: List[Dict[str, Any]]):
        self.packets = packets

    @abstractmethod
    def adapt_packets(self) -> List[Dict[str, Any]]:
        pass


class ContainerAdapterPurpleair(ContainerAdapter):

    def __init__(self, packets: List[Dict[str, Any]]):
        super().__init__(packets)

    def adapt_packets(self) -> List[Dict[str, Any]]:

        new_packets = []
        for packet in self.packets:

            # new packet compliant with sql container interface
            point = PostGISPointFactory(lat=packet['latitude'], lng=packet['longitude']).create_geometry()
            new_packet = {"name": f"{packet['name']} ({packet['sensor_index']})",
                          'type': 'purpleair',
                          'timestamp': DatetimeParser.current_sqltimestamp(),
                          'geometry': point.get_database_string(),
                          'param_name': ['primary_id_a', 'primary_id_b', 'primary_key_a', 'primary_key_b',
                                         'secondary_id_a', 'secondary_id_b', 'secondary_key_a', 'secondary_key_b',
                                         'primary_timestamp_a', 'primary_timestamp_b', 'secondary_timestamp_a',
                                         'secondary_timestamp_b'],
                          'param_value': [packet['primary_id_a'], packet['primary_id_b'], packet['primary_key_a'],
                                          packet['primary_key_b'], packet['secondary_id_a'], packet['secondary_id_b'],
                                          packet['secondary_key_a'], packet['secondary_key_b'],
                                          'null', 'null', 'null', 'null']}
            new_packets.append(new_packet)
        return new_packets


class ContainerAdapterFactory(object):

    def __init__(self, container_adapter_class=ContainerAdapter):
        self.container_adapter_class = container_adapter_class

    def make_container_adapter(self, packets: List[Dict[str, Any]]) -> ContainerAdapter:
        return self.container_adapter_class(packets=packets)
