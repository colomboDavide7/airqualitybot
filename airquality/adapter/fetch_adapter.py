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
        try:
            return {'channel_id': {'name': 'channel_id', 'val': packet['id']},
                    'channel_key': {'name': 'api_key', 'val': packet['key']},
                    'channel_ts': {'name': 'start', 'val': packet['ts']},
                    'ts_name': packet['ts_name']}
        except KeyError as ke:
            raise SystemExit(f"{EXCEPTION_HEADER} {FetchAdapterThingspeak.__name__} missing key='{ke!s}'.")


class FetchAdapterAtmotube(FetchAdapter):

    def adapt_packet(self, packet: Dict[str, Any]) -> Dict[str, Any]:
        try:
            return {'channel_id': {'name': 'mac', 'val': packet['mac']},
                    'channel_key': {'name': 'api_key', 'val': packet['api_key']},
                    'channel_ts': {'name': 'date', 'val': packet['date']}}
        except KeyError as ke:
            raise SystemExit(f"{EXCEPTION_HEADER} {FetchAdapterThingspeak.__name__} missing key='{ke!s}'.")


class FetchAdapterFactory:

    def __init__(self, fetch_adapter_class=FetchAdapter):
        self.adapter_class = fetch_adapter_class

    def make_adapter(self) -> FetchAdapter:
        return self.adapter_class()
