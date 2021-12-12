######################################################
#
# Author: Davide Colombo
# Date: 11/12/21 17:57
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
import os

import airquality.env.fact as factabc


class APIEnvFact(factabc.EnvFactory, abc.ABC):

    def __init__(self, path_to_env: str, command_name: str, command_type: str):
        super(APIEnvFact, self).__init__(path_to_env=path_to_env, command_type=command_type, command_name=command_name)

    @property
    def url(self) -> str:
        return os.environ[f'{self.command_type}_url']

    @property
    def fmt(self) -> str:
        return os.environ[f'{self.command_type}_response_fmt']
