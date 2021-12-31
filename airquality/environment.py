######################################################
#
# Author: Davide Colombo
# Date: 31/12/21 16:32
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import os
from typing import Tuple


class Environment(object):

    def __init__(self, personality: str):
        self._valid_pers = ()
        if personality not in self.valid_personalities:
            raise ValueError(f"{type(self).__name__} expected '{personality}' to be one of {self.valid_personalities}")
        self.personality = personality

    @property
    def valid_personalities(self) -> Tuple[str]:
        if not self._valid_pers:
            self._valid_pers = tuple([p for p in os.environ['valid_personalities'].split(',')])
        return self._valid_pers

    @property
    def program_usage_msg(self) -> str:
        pers = ' | '.join(f"{p}" for p in self.valid_personalities)
        return os.environ['program_usage_msg'].format(pers=pers)

    @property
    def url_template(self) -> str:
        return os.environ[f'{self.personality}_url']

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
