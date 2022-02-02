######################################################
#
# Author: Davide Colombo
# Date: 31/12/21 16:32
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import os
from typing import Tuple
from dotenv import load_dotenv
from airquality.extra.singleton import Singleton


_LOGGING_DIR_PERMISSION = 0o600         # only the user can read/write from that directory.


def get_environ(**kwargs):
    """
    A function that return the Singleton Environment instance or creates a new one if not exists.
    """

    return Environment(**kwargs)


class Environment(object, metaclass=Singleton):
    """
    A class that defines the interface for application environment interactions.

    Keyword arguments:
        *env_path*:         the full path to the environment file.

    Raises:
        *MissingEnvironPropertyError*       when this class failed to get property from the environment.

    """

    def __init__(self, env_path='.env'):
        self._env_path = env_path
        load_dotenv(dotenv_path=self._env_path)
        self._valid_pers = ()

    def _secure_get_from_environ(self, property_name: str):
        property_val = os.environ.get(property_name, None)
        if property_val is None:
            raise KeyError(f"Cannot found '{property_name}' in '{self._env_path}'")
        return property_val

# =========== APPLICATION PROPERTIES
    @property
    def valid_personalities(self) -> Tuple[str]:
        if not self._valid_pers:
            self._valid_pers = tuple([p for p in self._secure_get_from_environ('valid_personalities').split(',')])
        return self._valid_pers

    @property
    def program_usage_msg(self) -> str:
        pers = ' | '.join(f"{p}" for p in self.valid_personalities)
        return f"USAGE: {self._secure_get_from_environ('program_usage_msg').format(pers=pers)}"

# =========== LOG DIRECTORIES
    def logging_dir_of(self, personality: str) -> str:
        dirpath = f"{self._logging_dir()}/{personality}"
        if not os.path.exists(dirpath):
            os.mkdir(
                path=dirpath,
                mode=_LOGGING_DIR_PERMISSION
            )
        return dirpath

    def _logging_dir(self) -> str:
        return self._secure_get_from_environ(property_name="logging_dir")

# =========== RESOURCE DIRECTORIES
    def input_dir_of(self, personality: str) -> str:
        return f"{self._resource_dir()}/{personality}"

    def _resource_dir(self) -> str:
        return self._secure_get_from_environ('resource_dir')

# =========== API SERVER URLS
    def url_template(self, personality: str) -> str:
        return self._secure_get_from_environ(f'{personality}_url')

# =========== DATABASE CONNECTION PROPERTIES
    @property
    def dbname(self) -> str:
        return self._secure_get_from_environ('dbname')

    @property
    def dbuser(self) -> str:
        return self._secure_get_from_environ('user')

    @property
    def dbpwd(self) -> str:
        return self._secure_get_from_environ('password')

    @property
    def dbhost(self) -> str:
        return self._secure_get_from_environ('host')

    @property
    def dbport(self) -> str:
        return self._secure_get_from_environ('port')
