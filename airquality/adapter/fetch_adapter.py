######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 07/11/21 09:36
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any, List
from abc import ABC, abstractmethod
from airquality.constants.shared_constants import EXCEPTION_HEADER


class FetchAdapter(ABC):

    @abstractmethod
    def adapt_packet(self, packet: Dict[str, Any]) -> List[Dict[str, Any]]:
        pass


class FetchAdapterThingspeak(FetchAdapter):

    def adapt_packet(self, packet: Dict[str, Any]) -> List[Dict[str, Any]]:
        adapted_packets = []
        try:
            adapted_packets.append(
                {'channel_id': {'name': 'channel_id', 'val': packet['primary_id_a']},
                 'channel_key': {'name': 'api_key', 'val': packet['primary_key_a']},
                 'channel_ts': {'name': 'start', 'val': packet['primary_timestamp_a']}}
            )
            adapted_packets.append(
                {'channel_id': {'name': 'channel_id', 'val': packet['primary_id_b']},
                 'channel_key': {'name': 'api_key', 'val': packet['primary_key_b']},
                 'channel_ts': {'name': 'start', 'val': packet['primary_timestamp_b']}}
            )
            adapted_packets.append(
                {'channel_id': {'name': 'channel_id', 'val': packet['secondary_id_a']},
                 'channel_key': {'name': 'api_key', 'val': packet['secondary_key_a']},
                 'channel_ts': {'name': 'start', 'val': packet['secondary_timestamp_a']}}
            )
            adapted_packets.append(
                {'channel_id': {'name': 'channel_id', 'val': packet['secondary_id_b']},
                 'channel_key': {'name': 'api_key', 'val': packet['secondary_key_b']},
                 'channel_ts': {'name': 'start', 'val': packet['secondary_timestamp_b']}}
            )
        except KeyError as ke:
            raise SystemExit(f"{EXCEPTION_HEADER} {FetchAdapterThingspeak.__name__} missing key='{ke!s}'.")
        return adapted_packets


class FetchAdapterAtmotube(FetchAdapter):

    def adapt_packet(self, packet: Dict[str, Any]) -> List[Dict[str, Any]]:
        adapted_packets = []
        try:
            adapted_packets.append(
                {'channel_id': {'name': 'mac', 'val': packet['mac']},
                 'channel_key': {'name': 'api_key', 'val': packet['api_key']},
                 'channel_ts': {'name': 'date', 'val': packet['date']}}
            )
        except KeyError as ke:
            raise SystemExit(f"{EXCEPTION_HEADER} {FetchAdapterThingspeak.__name__} missing key='{ke!s}'.")
        return adapted_packets


class FetchAdapterFactory:

    def __init__(self, fetch_adapter_class=FetchAdapter):
        self.adapter_class = fetch_adapter_class

    def make_adapter(self):
        return self.adapter_class()
