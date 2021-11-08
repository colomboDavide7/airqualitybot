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


class UniversalAPIAdapter(ABC):

    @abstractmethod
    def adapt(self, api_param: Dict[str, Any]) -> List[Dict[str, Any]]:
        pass


class ThingspeakUniversalAPIAdapter(UniversalAPIAdapter):

    def adapt(self, api_param: Dict[str, Any]) -> List[Dict[str, Any]]:
        universal_api_packets = []
        try:
            universal_api_packets.append({'channel_id': {'name': 'channel_id', 'val': api_param['primary_id_a']},
                                          'channel_key': {'name': 'api_key', 'val': api_param['primary_key_a']}}
                                         )
            universal_api_packets.append({'channel_id': {'name': 'channel_id', 'val': api_param['primary_id_b']},
                                          'channel_key': {'name': 'api_key', 'val': api_param['primary_key_b']}}
                                         )
            universal_api_packets.append({'channel_id': {'name': 'channel_id', 'val': api_param['secondary_id_a']},
                                          'channel_key': {'name': 'api_key', 'val': api_param['secondary_key_a']}}
                                         )
            universal_api_packets.append({'channel_id': {'name': 'channel_id', 'val': api_param['secondary_id_b']},
                                          'channel_key': {'name': 'api_key', 'val': api_param['secondary_key_b']}}
                                         )
        except KeyError as ke:
            raise SystemExit(f"{EXCEPTION_HEADER} {ThingspeakUniversalAPIAdapter.__name__} missing key='{ke!s}'.")
        return universal_api_packets


class AtmotubeUniversalAPIAdapter(UniversalAPIAdapter):

    def adapt(self, api_param: Dict[str, Any]) -> List[Dict[str, Any]]:
        universal_api_packets = []
        try:
            universal_api_packets.append({'channel_id': {'name': 'mac', 'val': api_param['mac']},
                                          'channel_key': {'name': 'api_key', 'val': api_param['api_key']}}
                                         )
        except KeyError as ke:
            raise SystemExit(f"{EXCEPTION_HEADER} {AtmotubeUniversalAPIAdapter.__name__} missing key='{ke!s}'.")
        return universal_api_packets
