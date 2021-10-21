#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 16:42
# @Description: This script defines the DatabaseSettingsBuilder class
#
#################################################
import builtins
from typing import Dict, Any, List

SERVER_SETTINGS = "server"
USERS_SETTINGS  = "users"
LOGGER_SETTINGS = "logger"
MODELS_SETTINGS = "models"

AVAILABLE_MODELS = ["mobile", "station"]


class DatabaseSettingsBuilder(builtins.object):
    """
    Class that defines the @staticmethods for building correct setting
    dictionaries from the main one that holds all the parsed resource."""

    @staticmethod
    def create_db_settings_from_parsed_resources_for_user(
        parsed_resources: Dict[str, Any],
        username: str
    ) -> Dict[str, Any]:
        """
        Static method that builds the database settings from the parsed
        resources passed by the ResourceLoader.

        DatabaseConnectionAdapter needs the server information, the username and the
        corresponding password. This method copies the server settings from the
        parsed resources and add username and password fields."""

        if parsed_resources.get(USERS_SETTINGS, None) is None:
            raise SystemExit(f"{DatabaseSettingsBuilder.__name__}: "
                             f"missing '{USERS_SETTINGS}' section in resource file in method "
                             f"'{DatabaseSettingsBuilder.create_db_settings_from_parsed_resources_for_user.__name__}()'."
                             f"Check your 'properties/resources.json' file.")

        if parsed_resources.get(SERVER_SETTINGS, None) is None:
            raise SystemExit(f"{DatabaseSettingsBuilder.__name__}: "
                             f"missing '{SERVER_SETTINGS}' section in resource file in method "
                             f"'{DatabaseSettingsBuilder.create_db_settings_from_parsed_resources_for_user.__name__}()'."
                             f"Check your 'properties/resources.json' file.")

        if username not in parsed_resources[USERS_SETTINGS].keys():
            raise SystemExit(f"{DatabaseSettingsBuilder.__name__}: "
                             f"don't recognize username '{username}' in method "
                             f"'{DatabaseSettingsBuilder.create_db_settings_from_parsed_resources_for_user.__name__}()'."
                             f"Check your 'properties/resources.json' file.")


        settings = parsed_resources[SERVER_SETTINGS].copy()
        settings["username"] = username
        settings["password"] = parsed_resources[USERS_SETTINGS][f"{username}"]
        return settings


    @staticmethod
    def list_models_from_type(
        parsed_resources: Dict[str, Any],
        sensor_type: str
    ) -> List[str]:
        """This method returns the list of all sensor models based on sensor type
        defines in the 'models' section of the 'properties/resources.json' file.

        If 'models' section is missing in 'properties/resources.json' file,
        SystemExit exception is raised.

        If sensor_type is invalid, SystemExit exception is raised.
        """

        if parsed_resources.get(MODELS_SETTINGS, None) is None:
            raise SystemExit(f"{DatabaseSettingsBuilder.__name__}: "
                             f"missing '{MODELS_SETTINGS}' section in resource file in method "
                             f"'{DatabaseSettingsBuilder.list_models_from_type.__name__}()'."
                             f"Check your 'properties/resources.json' file.")

        if sensor_type not in parsed_resources[MODELS_SETTINGS].keys():
            raise SystemExit(f"{DatabaseSettingsBuilder.__name__}: "
                             f"don't recognize sensor type '{sensor_type}' in method "
                             f"'{DatabaseSettingsBuilder.list_models_from_type.__name__}()'."
                             f"Check your 'properties/resources.json' file.")

        return parsed_resources[MODELS_SETTINGS][f"{sensor_type}"]

