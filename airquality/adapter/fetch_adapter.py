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
        channel_id = channel_key = channel_ts = channel_name = ''
        id_set = key_set = ts_set = False
        # Search keys, no exact match
        for key in packet.keys():
            if 'id' in key:
                channel_id = packet[key]
                id_set = True
            elif 'key' in key:
                channel_key = packet[key]
                key_set = True
            elif 'timestamp' in key:
                channel_ts = packet[key]
                channel_name = key
                ts_set = True

        if not (id_set and key_set and ts_set):
            raise SystemExit(f"{EXCEPTION_HEADER} {FetchAdapterThingspeak.__name__} => id_set={id_set}, key_set={key_set}, "
                             f"ts_set={ts_set}.")

        # Adapt the packets to the new interface that uses the keys below
        adapted_packet['channel_id'] = channel_id
        adapted_packet['channel_key'] = channel_key
        adapted_packet['channel_ts'] = channel_ts
        adapted_packet['channel_name'] = channel_name
        return adapted_packet


class FetchAdapterFactory:

    def __init__(self, fetch_adapter_class=FetchAdapter):
        self.adapter_class = fetch_adapter_class

    def make_adapter(self):
        return self.adapter_class()
