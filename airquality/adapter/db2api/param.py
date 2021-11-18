######################################################
#
# Author: Davide Colombo
# Date: 12/11/21 17:12
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import Dict, Any, List
import airquality.adapter.config as c


def get_param_adapter(sensor_type: str):
    if sensor_type == 'atmotube':
        return AtmotubeParamAdapter()
    elif sensor_type == 'thingspeak':
        return ThingspeakParamAdapter()
    else:
        raise SystemExit(f"'{get_param_adapter.__name__}():' bad type {sensor_type}")


################################ PARAM ADAPTER BASE CLASS ################################
class ParamAdapter(abc.ABC):

    @abc.abstractmethod
    def reshape(self, database_api_param: Dict[str, Any]) -> List[Dict[str, Any]]:
        pass

    @abc.abstractmethod
    def _exit_on_missing_parameters(self, database_api_param: Dict[str, Any]):
        pass


################################ THINGSPEAK PARAM ADAPTER ################################
class ThingspeakParamAdapter(ParamAdapter):

    def reshape(self, database_api_param: Dict[str, Any]) -> List[Dict[str, Any]]:
        self._exit_on_missing_parameters(database_api_param)
        return [{c.CH_ID: database_api_param['primary_id_a'],
                 c.API_KEY: database_api_param['primary_key_a'],
                 c.CH_NAME: c.FST_CH_A},
                {c.CH_ID: database_api_param['primary_id_b'],
                 c.API_KEY: database_api_param['primary_key_b'],
                 c.CH_NAME: c.FST_CH_B},
                {c.CH_ID: database_api_param['secondary_id_a'],
                 c.API_KEY: database_api_param['secondary_key_a'],
                 c.CH_NAME: c.SND_CH_A},
                {c.CH_ID: database_api_param['secondary_id_b'],
                 c.API_KEY: database_api_param['secondary_key_b'],
                 c.CH_NAME: c.SND_CH_B}]

    def _exit_on_missing_parameters(self, database_api_param: Dict[str, Any]):
        if 'primary_id_a' not in database_api_param or 'primary_key_a' not in database_api_param:
            raise SystemExit(f"{ThingspeakParamAdapter.__name__}: bad api_param => missing primary channel A data")
        elif 'primary_id_b' not in database_api_param or 'primary_key_b' not in database_api_param:
            raise SystemExit(f"{ThingspeakParamAdapter.__name__}: bad api_param => missing primary channel B data")
        elif 'secondary_id_a' not in database_api_param or 'secondary_key_a' not in database_api_param:
            raise SystemExit(f"{ThingspeakParamAdapter.__name__}: bad api_param => missing secondary channel A data")
        elif 'secondary_id_b' not in database_api_param or 'secondary_key_b' not in database_api_param:
            raise SystemExit(f"{ThingspeakParamAdapter.__name__}: bad api_param => missing secondary channel B data")


################################ ATMOTUBE PARAM ADAPTER ################################
class AtmotubeParamAdapter(ParamAdapter):

    def reshape(self, database_api_param: Dict[str, Any]) -> List[Dict[str, Any]]:
        self._exit_on_missing_parameters(database_api_param)
        return [{c.MAC_ADDR: database_api_param['mac'],
                 c.API_KEY: database_api_param['api_key'],
                 c.CH_NAME: "main"}]

    def _exit_on_missing_parameters(self, database_api_param: Dict[str, Any]):
        if 'api_key' not in database_api_param:
            raise SystemExit(f"{AtmotubeParamAdapter.__name__}: bad api_param => missing key='api_key'")
        elif 'mac' not in database_api_param:
            raise SystemExit(f"{AtmotubeParamAdapter.__name__}: bad api_param => missing key='mac'")
