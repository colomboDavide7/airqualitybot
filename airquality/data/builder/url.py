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

EQ = '='
AND = '&'
QU = '?'


class URLBuilder(ABC):

    def __init__(self, api_address: str):
        self.api_address = api_address

    @abstractmethod
    def url(self) -> str:
        pass


class PurpleairURLBuilder(URLBuilder):

    def __init__(self, api_address: str, parameters: Dict[str, Any]):
        super().__init__(api_address=api_address)
        try:
            self.api_key = parameters.pop('api_key')
            self.fields = parameters.pop('fields')
            self.opt_param = parameters
        except KeyError as ke:
            raise SystemExit(
                f"{EXCEPTION_HEADER} {PurpleairURLBuilder.__name__} bad 'api.json' file structure => missing key={ke!s}"
            )

    def url(self) -> str:
        if not self.fields:
            raise SystemExit(
                f"{EXCEPTION_HEADER} {PurpleairURLBuilder.__name__} bad 'api.json' file structure => empty fields."
            )

        url = self.api_address + QU
        url += 'api_key' + EQ + self.api_key + AND
        url += 'fields' + EQ

        for field in self.fields:
            url += field + ','
        url = url.strip(',') + AND

        for param_name, param_value in self.opt_param.items():
            url += param_name + EQ + param_value + AND

        return url.strip(AND)


class URLBuilderAtmotube(URLBuilder):

    def __init__(self, api_address: str, parameters: Dict[str, Any]):
        super().__init__(api_address=api_address, parameters=parameters)

    def url(self) -> str:

        self.raise_system_exit_when_is_missing_param(param2find='api_key')
        self.raise_system_exit_when_is_missing_param(param2find='mac')

        url = self.api_address + '?'
        for param_name, param_value in self.parameters.items():
            url += param_name + '=' + param_value + '&'
        return url.strip('&')


class URLBuilderThingspeak(URLBuilder):

    def __init__(self, api_address: str, parameters: Dict[str, Any]):
        super().__init__(api_address=api_address, parameters=parameters)

    def url(self) -> str:

        self.raise_system_exit_when_is_missing_param(param2find='channel_id')
        self.raise_system_exit_when_is_missing_param(param2find='format')
        self.raise_system_exit_when_is_missing_param(param2find='api_key')
        ans_format = self.parameters.pop('format')
        url = self.api_address + '/' + self.parameters.pop('channel_id') + '/'
        url += 'feeds.' + ans_format + '?'
        for param_name, param_value in self.parameters.items():
            url += param_name + '=' + param_value + '&'
        # Insert again the format into the parameters for the other channels
        self.parameters['format'] = ans_format
        return url.strip('&')
