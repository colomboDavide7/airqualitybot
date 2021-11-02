#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 16:42
# @Description: this script defines a class for picking resources from all the parsed resources.
#
#################################################
import builtins
from typing import Dict, Any, List
from airquality.constants.shared_constants import PURPLE_AIR_API_PARAM, PURPLE_AIR_GEO_PARAM, EMPTY_LIST, \
    MOBILE_SENSOR_PERSONALITIES, PURPLEAIR_SENSOR_IDX_PARAM, PURPLEAIR_NAME_PARAM, \
    ATMOTUBE_DATE_PARAM, ATMOTUBE_PERSONALITY, PURPLEAIR_PERSONALITY, ATMOTUBE_OPTIONAL_API_PARAM

LOGGER_SECTION = "logger"
SERVER_SECTION = "server"
PERSONALITY_SECTION = "personality"
API_ADDRESS_SECTION = "api_address"


class ResourcePicker(builtins.object):

    @classmethod
    def pick_db_conn_properties(cls, parsed_resources: Dict[str, Any], bot_personality: str) -> Dict[str, Any]:
        """Class method that picks the database properties from the parsed resources.

        If 'server' section is missing in 'properties/resources.json' file, SystemExit exception is raised.
        If 'bot_personality' is invalid, SystemExit exception is raised."""

        if parsed_resources.get(PERSONALITY_SECTION, None) is None:
            raise SystemExit(f"{ResourcePicker.__name__}: "
                             f"missing '{PERSONALITY_SECTION}' section in resource file in method "
                             f"'{ResourcePicker.pick_db_conn_properties.__name__}()'."
                             f"Check your 'properties/resources.json' file.")

        if parsed_resources.get(SERVER_SECTION, None) is None:
            raise SystemExit(f"{ResourcePicker.__name__}: "
                             f"missing '{SERVER_SECTION}' section in resource file in method "
                             f"'{ResourcePicker.pick_db_conn_properties.__name__}()'."
                             f"Check your 'properties/resources.json' file.")

        if bot_personality not in parsed_resources[PERSONALITY_SECTION].keys():
            raise SystemExit(f"{ResourcePicker.__name__}: "
                             f"don't recognize personality '{bot_personality}' in method "
                             f"'{ResourcePicker.pick_db_conn_properties.__name__}()'."
                             f"Check your 'properties/resources.json' file.")

        settings = parsed_resources[SERVER_SECTION].copy()
        settings["username"] = parsed_resources[PERSONALITY_SECTION][f"{bot_personality}"]["username"]
        settings["password"] = parsed_resources[PERSONALITY_SECTION][f"{bot_personality}"]["password"]
        return settings

    @classmethod
    def pick_api_address_from_number(cls, parsed_resources: Dict[str, Any], bot_personality: str,
                                     api_address_number: str) -> str:

        if parsed_resources.get(API_ADDRESS_SECTION, None) is None:
            raise SystemExit(f"{ResourcePicker.__name__}: "
                             f"missing '{API_ADDRESS_SECTION}' section in resource file in method "
                             f"'{ResourcePicker.pick_api_address_from_number.__name__}()'."
                             f"Check your 'properties/resources.json' file.")

        if bot_personality not in parsed_resources[API_ADDRESS_SECTION].keys():
            raise SystemExit(f"{ResourcePicker.__name__}: "
                             f"don't recognize personality '{bot_personality}' in method "
                             f"'{ResourcePicker.pick_api_address_from_number.__name__}()'."
                             f"Check your 'properties/resources.json' file.")

        if api_address_number not in parsed_resources[API_ADDRESS_SECTION][f"{bot_personality}"].keys():
            raise SystemExit(f"{ResourcePicker.__name__}: "
                             f"don't recognize api address number '{bot_personality}' in method "
                             f"'{ResourcePicker.pick_api_address_from_number.__name__}()'."
                             f"Check your 'properties/resources.json' file.")

        return parsed_resources[API_ADDRESS_SECTION][f"{bot_personality}"][f"{api_address_number}"]

    @classmethod
    def pick_api_param_filter_list_from_personality(cls, bot_personality: str) -> List[str]:

        if bot_personality == "purpleair":
            return PURPLE_AIR_API_PARAM
        else:
            return EMPTY_LIST

    @classmethod
    def pick_geo_param_filter_list_from_personality(cls, personality: str) -> List[str]:
        if personality == "purpleair":
            return PURPLE_AIR_GEO_PARAM
        else:
            return EMPTY_LIST

    @classmethod
    def pick_last_timestamp_from_api_param_by_personality(cls, api_param: Dict[str, Any], personality: str) -> str:

        if personality not in MOBILE_SENSOR_PERSONALITIES:
            raise SystemExit(f"{ResourcePicker.pick_last_timestamp_from_api_param_by_personality.__name__}: "
                             f"cannot call this method with personality = '{personality}'.")

        sqltimestamp = ""
        if personality == ATMOTUBE_PERSONALITY:
            if api_param.get(ATMOTUBE_DATE_PARAM, None) is not None:
                sqltimestamp = api_param[ATMOTUBE_DATE_PARAM]

        return sqltimestamp

    @classmethod
    def pick_sensor_name_from_identifier(cls, packet: Dict[str, Any], personality: str) -> str:

        if personality == PURPLEAIR_PERSONALITY:
            return f"{packet[PURPLEAIR_NAME_PARAM]} ({packet[PURPLEAIR_SENSOR_IDX_PARAM]})"
        else:
            raise SystemExit(f"{ResourcePicker.pick_sensor_name_from_identifier.__name__}: cannot pick name for "
                             f"personality = '{personality}'.")

    @classmethod
    def pick_optional_api_parameters_from_api_data(cls, personality: str) -> List[str]:

        if personality == ATMOTUBE_PERSONALITY:
            return ATMOTUBE_OPTIONAL_API_PARAM
        else:
            raise SystemExit(f"{ResourcePicker.pick_optional_api_parameters_from_api_data.__name__}: "
                             f"cannot pick optional API parameters for personality = '{personality}'.")
