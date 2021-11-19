######################################################
#
# Author: Davide Colombo
# Date: 12/11/21 17:12
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import Dict, Any, List
import airquality.adapter.config as adapt_const


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
        return [{adapt_const.CH_ID: database_api_param[adapt_const.FST_ID_A],
                 adapt_const.API_KEY: database_api_param[adapt_const.FST_KEY_A],
                 adapt_const.CH_NAME: adapt_const.FST_CH_A},
                {adapt_const.CH_ID: database_api_param[adapt_const.FST_ID_B],
                 adapt_const.API_KEY: database_api_param[adapt_const.FST_KEY_B],
                 adapt_const.CH_NAME: adapt_const.FST_CH_B},
                {adapt_const.CH_ID: database_api_param[adapt_const.SND_ID_A],
                 adapt_const.API_KEY: database_api_param[adapt_const.SND_KEY_A],
                 adapt_const.CH_NAME: adapt_const.SND_CH_A},
                {adapt_const.CH_ID: database_api_param[adapt_const.SND_ID_B],
                 adapt_const.API_KEY: database_api_param[adapt_const.SND_KEY_B],
                 adapt_const.CH_NAME: adapt_const.SND_CH_B}]

    def _exit_on_missing_parameters(self, database_api_param: Dict[str, Any]):
        for n in adapt_const.API_PARAM:
            if n not in database_api_param:
                raise SystemExit(f"{ThingspeakParamAdapter.__name__}: bad database api param => missing key='{n}'")


################################ ATMOTUBE PARAM ADAPTER ################################
class AtmotubeParamAdapter(ParamAdapter):

    def reshape(self, database_api_param: Dict[str, Any]) -> List[Dict[str, Any]]:
        self._exit_on_missing_parameters(database_api_param)

        return [{adapt_const.MAC_ADDR: database_api_param['mac'],
                 adapt_const.API_KEY: database_api_param['api_key'],
                 adapt_const.CH_NAME: adapt_const.ATMOTUBE_CHANNEL}]

    def _exit_on_missing_parameters(self, database_api_param: Dict[str, Any]):
        if 'api_key' not in database_api_param:
            raise SystemExit(f"{AtmotubeParamAdapter.__name__}: bad api_param => missing key='api_key'")
        elif 'mac' not in database_api_param:
            raise SystemExit(f"{AtmotubeParamAdapter.__name__}: bad api_param => missing key='mac'")
