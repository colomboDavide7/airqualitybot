######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 07/11/21 09:36
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import Dict, Any, List
from airquality.core.constants.shared_constants import EXCEPTION_HEADER

CH = 'channel_id'
KEY = 'api_key'
MAC = 'mac'


class UniformReshaper(abc.ABC):

    @abc.abstractmethod
    def db2api(self, api_param: Dict[str, Any]) -> List[Dict[str, Any]]:
        pass


class ThingspeakUniformReshaper(UniformReshaper):

    def db2api(self, api_param: Dict[str, Any]) -> List[Dict[str, Any]]:
        uniform_packets = []
        try:
            uniform_packets.append({CH: api_param['primary_id_a'],
                                    KEY: api_param['primary_key_a']})
            uniform_packets.append({CH: api_param['primary_id_b'],
                                    KEY: api_param['primary_key_b']})
            uniform_packets.append({CH: api_param['secondary_id_a'],
                                    KEY: api_param['secondary_key_a']})
            uniform_packets.append({CH: api_param['secondary_id_b'],
                                    KEY: api_param['secondary_key_b']})
        except KeyError as ke:
            raise SystemExit(f"{EXCEPTION_HEADER} {ThingspeakUniformReshaper.__name__} missing key={ke!s}.")
        return uniform_packets


class AtmotubeUniformReshaper(UniformReshaper):

    def db2api(self, api_param: Dict[str, Any]) -> List[Dict[str, Any]]:
        uniform_packets = []
        try:
            uniform_packets.append({MAC: api_param['mac'],
                                    KEY: api_param['api_key']})
        except KeyError as ke:
            raise SystemExit(f"{EXCEPTION_HEADER} {AtmotubeUniformReshaper.__name__} missing key={ke!s}.")
        return uniform_packets
