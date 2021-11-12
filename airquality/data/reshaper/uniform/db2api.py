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

CH_ID = 'channel_id'
CH_NM = 'channel_name'
KEY = 'api_key'
MAC = 'mac'


def get_db2api_reshaper_class(sensor_type: str):

    if sensor_type == 'atmotube':
        return AtmotubeUniformReshaper
    elif sensor_type == 'thingspeak':
        return ThingspeakUniformReshaper
    else:
        raise SystemExit(
            f"{get_db2api_reshaper_class.__name__}: bad type => DB2API UniformReshaper is not defined for '{sensor_type}'")


class UniformReshaper(abc.ABC):

    def __init__(self, api_param: Dict[str, Any]):
        self.api_param = api_param

    @abc.abstractmethod
    def reshape(self) -> List[Dict[str, Any]]:
        pass


class ThingspeakUniformReshaper(UniformReshaper):

    def __init__(self, api_param: Dict[str, Any]):
        super(ThingspeakUniformReshaper, self).__init__(api_param)

    def reshape(self) -> List[Dict[str, Any]]:
        uniform_packets = []
        try:
            uniform_packets.append({CH_ID: self.api_param['primary_id_a'],
                                    KEY: self.api_param['primary_key_a'],
                                    CH_NM: "1A"})
            uniform_packets.append({CH_ID: self.api_param['primary_id_b'],
                                    KEY: self.api_param['primary_key_b'],
                                    CH_NM: "1B"})
            uniform_packets.append({CH_ID: self.api_param['secondary_id_a'],
                                    KEY: self.api_param['secondary_key_a'],
                                    CH_NM: "2A"})
            uniform_packets.append({CH_ID: self.api_param['secondary_id_b'],
                                    KEY: self.api_param['secondary_key_b'],
                                    CH_NM: "2B"})
        except KeyError as ke:
            raise SystemExit(f"{ThingspeakUniformReshaper.__name__} missing key={ke!s}.")
        return uniform_packets


class AtmotubeUniformReshaper(UniformReshaper):

    def __ini__(self, api_param: Dict[str, Any]):
        super(AtmotubeUniformReshaper, self).__init__(api_param)

    def reshape(self) -> List[Dict[str, Any]]:
        uniform_packets = []
        try:
            uniform_packets.append({MAC: self.api_param['mac'],
                                    KEY: self.api_param['api_key'],
                                    CH_NM: "Main"})
        except KeyError as ke:
            raise SystemExit(f"{AtmotubeUniformReshaper.__name__} missing key={ke!s}.")
        return uniform_packets
