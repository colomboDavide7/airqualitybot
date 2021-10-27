#################################################
#
# @Author: davidecolombo
# @Date: mer, 27-10-2021, 15:13
# @Description: this script defines the classes for reshaping data coming from database in order to make them compliant
#               with API needs.
#
#################################################
import builtins
from typing import Dict, Any
from abc import ABC, abstractmethod
from airquality.constants.shared_constants import EMPTY_DICT, \
    THINGSPEAK_CH_ID_2PICK, THINGSPEAK_KEY_2PICK


class Database2APIReshaper(ABC):


    @abstractmethod
    def reshape_data(self, api_param: Dict[str, Any]) -> Dict[str, Any]:
        pass


class Database2APIReshaperThingspeak(Database2APIReshaper):


    def reshape_data(self, api_param: Dict[str, Any]) -> Dict[str, Any]:

        if api_param == EMPTY_DICT:
            raise SystemExit(f"{Database2APIReshaperThingspeak.__name__}: cannot reshape data when 'api_param' are missing.")

        reshaped = {}
        keys = api_param.keys()
        for i in range(len(THINGSPEAK_KEY_2PICK)):
            channel_key = THINGSPEAK_KEY_2PICK[i]
            if channel_key not in keys:
                raise SystemExit(f"{Database2APIReshaperThingspeak.__name__}: missing channel key = '{channel_key}'")
            channel_id = THINGSPEAK_CH_ID_2PICK[i]
            if channel_id not in keys:
                raise SystemExit(f"{Database2APIReshaperThingspeak.__name__}: missing channel id = '{channel_id}'")
            reshaped[api_param[channel_id]] = api_param[channel_key]
        return reshaped



################################ FACTORY ################################
class Database2APIReshaperFactory(builtins.object):


    @classmethod
    def create_reshaper(cls, bot_personality: str) -> Database2APIReshaper:

        if bot_personality == "thingspeak":
            return Database2APIReshaperThingspeak()
        else:
            raise SystemExit(f"{Database2APIReshaperFactory.__name__}: cannot instantiate {Database2APIReshaper.__name__} "
                             f"instance for personality='{bot_personality}'.")
