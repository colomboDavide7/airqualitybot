#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 16:42
# @Description: This script defines a class for picking particular resources
#               at the right moment from all the parsed resources.
#################################################
import builtins
from typing import Dict, Any, List

SERVER_SETTINGS = "server"
USERS_SETTINGS  = "users"
LOGGER_SETTINGS = "logger"
MODELS_SETTINGS = "models"

AVAILABLE_MODELS = ["mobile", "station"]


class ResourcePicker(builtins.object):


    @staticmethod
    def pick_db_conn_properties_from_user(parsed_resources: Dict[str, Any], username: str) -> Dict[str, Any]:
        """Static method that picks the database properties from the parsed resources.

        If 'server' section is missing in 'properties/resources.json' file, SystemExit exception is raised.

        If 'username' is invalid, SystemExit exception is raised."""

        if parsed_resources.get(USERS_SETTINGS, None) is None:
            raise SystemExit(f"{ResourcePicker.__name__}: "
                             f"missing '{USERS_SETTINGS}' section in resource file in method "
                             f"'{ResourcePicker.pick_db_conn_properties_from_user.__name__}()'."
                             f"Check your 'properties/resources.json' file.")

        if parsed_resources.get(SERVER_SETTINGS, None) is None:
            raise SystemExit(f"{ResourcePicker.__name__}: "
                             f"missing '{SERVER_SETTINGS}' section in resource file in method "
                             f"'{ResourcePicker.pick_db_conn_properties_from_user.__name__}()'."
                             f"Check your 'properties/resources.json' file.")

        if username not in parsed_resources[USERS_SETTINGS].keys():
            raise SystemExit(f"{ResourcePicker.__name__}: "
                             f"don't recognize username '{username}' in method "
                             f"'{ResourcePicker.pick_db_conn_properties_from_user.__name__}()'."
                             f"Check your 'properties/resources.json' file.")


        settings = parsed_resources[SERVER_SETTINGS].copy()
        settings["username"] = username
        settings["password"] = parsed_resources[USERS_SETTINGS][f"{username}"]
        return settings


    @staticmethod
    def pick_sensor_models_from_sensor_type(parsed_resources: Dict[str, Any], sensor_type: str) -> List[str]:
        """Static method that picks all sensor models within a sensor type from parsed resources.

        If 'models' section is missing in 'properties/resources.json' file, SystemExit exception is raised.

        If 'sensor_type' is invalid, SystemExit exception is raised."""

        if parsed_resources.get(MODELS_SETTINGS, None) is None:
            raise SystemExit(f"{ResourcePicker.__name__}: "
                             f"missing '{MODELS_SETTINGS}' section in resource file in method "
                             f"'{ResourcePicker.pick_sensor_models_from_sensor_type.__name__}()'."
                             f"Check your 'properties/resources.json' file.")

        if sensor_type not in parsed_resources[MODELS_SETTINGS].keys():
            raise SystemExit(f"{ResourcePicker.__name__}: "
                             f"don't recognize sensor type '{sensor_type}' in method "
                             f"'{ResourcePicker.pick_sensor_models_from_sensor_type.__name__}()'."
                             f"Check your 'properties/resources.json' file.")

        return parsed_resources[MODELS_SETTINGS][f"{sensor_type}"]
