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


class AppEnvironError(Exception):

    def __init__(self, cause: str):
        self.cause = cause

    def __repr__(self):
        return f"{type(self).__name__}(cause={self.cause})"


class Environment(object):
    """
    An *object* class a boundary interface for interacting with the external '.env' file.
    """

    def __init__(self):
        load_dotenv(dotenv_path='.env')
        self._valid_pers = ()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type == KeyError:
            raise AppEnvironError(cause=f"missing environment field {exc_val}")

    def url_template(self, personality: str) -> str:
        return os.environ[f'{personality}_url']

    def input_dir_of(self, personality: str) -> str:
        return f"{os.environ['resource_dir']}/{os.environ[f'{personality}_dir']}/{os.environ[f'{personality}_data_dir']}"

    @property
    def valid_personalities(self) -> Tuple[str]:
        if not self._valid_pers:
            self._valid_pers = tuple([p for p in os.environ['valid_personalities'].split(',')])
        return self._valid_pers

    @property
    def program_usage_msg(self) -> str:
        pers = ' | '.join(f"{p}" for p in self.valid_personalities)
        return f"USAGE: {os.environ['program_usage_msg'].format(pers=pers)}"

    @property
    def dbname(self) -> str:
        return os.environ['dbname']

    @property
    def user(self) -> str:
        return os.environ['user']

    @property
    def password(self) -> str:
        return os.environ['password']

    @property
    def host(self) -> str:
        return os.environ['host']

    @property
    def port(self) -> str:
        return os.environ['port']
