######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 07/11/21 09:36
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any
from abc import ABC, abstractmethod
from airquality.constants.shared_constants import EXCEPTION_HEADER


class FetchAdapter(ABC):

    @abstractmethod
    def adapt_packet(self, packet: Dict[str, Any]) -> Dict[str, Any]:
        pass


class FetchAdapterThingspeak(FetchAdapter):

    def adapt_packet(self, packet: Dict[str, Any]) -> Dict[str, Any]:
        adapted_packet = {}
        try:
            adapted_packet['channel_id'] = {'name': 'channel_id',
                                            'val': [packet['primary_id_a'], packet['primary_id_b'], packet['secondary_id_a'],
                                                    packet['secondary_id_b']]}

            adapted_packet['channel_key'] = {'name': 'api_key',
                                             'val': [packet['primary_key_a'], packet['primary_key_b'], packet['secondary_key_a'],
                                                     packet['secondary_key_b']]}

            adapted_packet['channel_ts'] = {'name': 'start',
                                            'val': [packet['primary_timestamp_a'], packet['primary_timestamp_b'],
                                                    packet['secondary_timestamp_a'], packet['secondary_timestamp_b']]}
            # adapted_packet['channel_name'] = ['1A', '1B', '2A', '2B']

        except KeyError as ke:
            raise SystemExit(f"{EXCEPTION_HEADER} {FetchAdapterThingspeak.__name__} missing key='{ke!s}'.")
        return adapted_packet


class FetchAdapterAtmotube(FetchAdapter):

    def adapt_packet(self, packet: Dict[str, Any]) -> Dict[str, Any]:
        adapted_packet = {}
        try:
            adapted_packet['channel_id'] = {'name': 'mac', 'val': packet['mac']}
            adapted_packet['channel_key'] = {'name': 'api_key', 'val': packet['api_key']}
            adapted_packet['channel_ts'] = {'name': 'date', 'val': packet['date']}
            # adapted_packet['channel_name'] = 'Atmotube sensor'

        except KeyError as ke:
            raise SystemExit(f"{EXCEPTION_HEADER} {FetchAdapterThingspeak.__name__} missing key='{ke!s}'.")
        return adapted_packet


class FetchAdapterFactory:

    def __init__(self, fetch_adapter_class=FetchAdapter):
        self.adapter_class = fetch_adapter_class

    def make_adapter(self):
        return self.adapter_class()
