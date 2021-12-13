######################################################
#
# Author: Davide Colombo
# Date: 11/12/21 17:57
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import os
import abc
import airquality.env.fact as factabc


# ------------------------------- APIEnvFactABC ------------------------------- #
class APIEnvFactABC(factabc.EnvFactABC, abc.ABC):

    def __init__(self, path_to_env: str, command: str, target: str):
        super(APIEnvFactABC, self).__init__(path_to_env=path_to_env, target=target, command=command)

    @property
    def url(self) -> str:
        return os.environ[f'{self.target}_url']

    @property
    def fmt(self) -> str:
        return os.environ[f'{self.target}_response_fmt']
