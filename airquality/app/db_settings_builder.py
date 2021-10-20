#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 16:42
# @Description: This script defines the DatabaseSettingsBuilder class
#
#################################################
import builtins
from typing import Dict, Any

SERVER_SETTINGS = "server"
USERS_SETTINGS  = "users"
LOGGER_SETTINGS = "logger"


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

        DatabaseConnection needed the server information, the username and the
        corresponding password. This method copies the server settings from the
        parsed resources and add username and password fields."""

        if parsed_resources.get(USERS_SETTINGS, None) is None:
            raise SystemExit(f"{DatabaseSettingsBuilder.__name__}: "
                             f"missing '{USERS_SETTINGS}' section in resource file in method "
                             f"'{DatabaseSettingsBuilder.create_db_settings_from_parsed_resources_for_user.__name__}()'.")

        if parsed_resources.get(SERVER_SETTINGS, None) is None:
            raise SystemExit(f"{DatabaseSettingsBuilder.__name__}: "
                             f"missing '{SERVER_SETTINGS}' section in resource file in method "
                             f"'{DatabaseSettingsBuilder.create_db_settings_from_parsed_resources_for_user.__name__}()'.")

        if username not in parsed_resources[USERS_SETTINGS].keys():
            raise SystemExit(f"{DatabaseSettingsBuilder.__name__}: "
                             f"don't recognize username '{username}' from resource file in method "
                             f"'{DatabaseSettingsBuilder.create_db_settings_from_parsed_resources_for_user.__name__}()'.")


        settings = parsed_resources[SERVER_SETTINGS].copy()
        settings["username"] = username
        settings["password"] = parsed_resources[USERS_SETTINGS][f"{username}"]
        return settings
