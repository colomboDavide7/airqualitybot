######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 12/11/21 17:12
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import Dict, Any, List

CH_ID = 'channel_id'
CH_NM = 'channel_name'
KEY = 'api_key'
MAC = 'mac'


def get_param_adapter_class(sensor_type: str):
    if sensor_type == 'atmotube':
        return AtmotubeParamAdapter
    elif sensor_type == 'thingspeak':
        return ThingspeakParamAdapter
    else:
        raise SystemExit(f"'{get_param_adapter_class.__name__}()': "
                         f"bad type => {ParamAdapter.__name__} undefined for type='{sensor_type}'")


class ParamAdapter(abc.ABC):

    def __init__(self, api_param: Dict[str, Any]):
        self.api_param = api_param

    @abc.abstractmethod
    def reshape(self) -> List[Dict[str, Any]]:
        pass


class ThingspeakParamAdapter(ParamAdapter):

    def __init__(self, api_param: Dict[str, Any]):
        super(ThingspeakParamAdapter, self).__init__(api_param)

    def reshape(self) -> List[Dict[str, Any]]:
        if 'primary_id_a' not in self.api_param or 'primary_key_a' not in self.api_param:
            raise SystemExit(f"{ThingspeakParamAdapter.__name__}: bad api_param => missing primary channel A data")
        elif 'primary_id_b' not in self.api_param or 'primary_key_b' not in self.api_param:
            raise SystemExit(f"{ThingspeakParamAdapter.__name__}: bad api_param => missing primary channel B data")
        elif 'secondary_id_a' not in self.api_param or 'secondary_key_a' not in self.api_param:
            raise SystemExit(f"{ThingspeakParamAdapter.__name__}: bad api_param => missing secondary channel A data")
        elif 'secondary_id_b' not in self.api_param or 'secondary_key_b' not in self.api_param:
            raise SystemExit(f"{ThingspeakParamAdapter.__name__}: bad api_param => missing secondary channel B data")

        return [{CH_ID: self.api_param['primary_id_a'],
                 KEY: self.api_param['primary_key_a'],
                 CH_NM: "1A"}, {CH_ID: self.api_param['primary_id_b'],
                                KEY: self.api_param['primary_key_b'],
                                CH_NM: "1B"}, {CH_ID: self.api_param['secondary_id_a'],
                                               KEY: self.api_param['secondary_key_a'],
                                               CH_NM: "2A"}, {CH_ID: self.api_param['secondary_id_b'],
                                                              KEY: self.api_param['secondary_key_b'],
                                                              CH_NM: "2B"}]


class AtmotubeParamAdapter(ParamAdapter):

    def __ini__(self, api_param: Dict[str, Any]):
        super(AtmotubeParamAdapter, self).__init__(api_param)

    def reshape(self) -> List[Dict[str, Any]]:
        if 'api_key' not in self.api_param:
            raise SystemExit(f"{AtmotubeParamAdapter.__name__}: bad api_param => missing key='api_key'")
        elif 'mac' not in self.api_param:
            raise SystemExit(f"{AtmotubeParamAdapter.__name__}: bad api_param => missing key='mac'")

        return [{MAC: self.api_param['mac'],
                 KEY: self.api_param['api_key'],
                 CH_NM: "main"}]
