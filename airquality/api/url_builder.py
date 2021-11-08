#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 09:52
# @Description: this script defines a simple factory class for building valid URL querystring based on sensor type.
#
#################################################
from typing import Dict, Any
from abc import ABC, abstractmethod
from airquality.constants.shared_constants import EXCEPTION_HEADER


class URLBuilder(ABC):

    def __init__(self, api_address: str, parameters: Dict[str, Any]):
        self.api_address = api_address
        self.parameters = parameters

    def raise_system_exit_when_is_missing_param(self, param2find: str):
        if param2find not in self.parameters.keys():
            raise SystemExit(f"{EXCEPTION_HEADER} missing '{param2find}' in '{URLBuilder.build_url.__name__}()' method.")

    @abstractmethod
    def build_url(self) -> str:
        pass


class URLBuilderPurpleair(URLBuilder):

    def __init__(self, api_address: str, parameters: Dict[str, Any]):
        super().__init__(api_address=api_address, parameters=parameters)

    def build_url(self) -> str:

        self.raise_system_exit_when_is_missing_param(param2find='api_key')
        self.raise_system_exit_when_is_missing_param(param2find='fields')
        if not self.parameters['fields']:
            raise SystemExit(f"{EXCEPTION_HEADER} bad 'api.json' file structure in '{URLBuilderPurpleair.__name__}' => "
                             f"'fields' param is empty.")

        url = self.api_address + '?'
        for param_name, param_value in self.parameters.items():
            if param_name == 'fields':
                url += 'fields' + '='
                for field in self.parameters[param_name]:
                    url += field + ','
                url = url.strip(',') + '&'
            else:
                url += param_name + '=' + param_value + '&'
        return url.strip('&')
