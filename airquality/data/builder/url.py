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


class AtmotubeURLBuilder(URLBuilder):

    def __init__(self, api_address: str, parameters: Dict[str, Any]):
        super().__init__(api_address=api_address)
        try:
            self.api_key = parameters.pop('api_key')
            self.mac = parameters.pop('mac')
            self.opt_param = parameters
        except KeyError as ke:
            raise SystemExit(
                f"{EXCEPTION_HEADER} {AtmotubeURLBuilder.__name__} bad 'api.json' file structure => missing key={ke!s}"
            )

    def url(self) -> str:
        url = self.api_address + QU
        url += 'api_key' + EQ + self.api_key + AND
        url += 'mac' + EQ + self.mac + AND
        for param_name, param_value in self.opt_param.items():
            url += param_name + EQ + param_value + AND
        return url.strip(AND)


class ThingspeakURLBuilder(URLBuilder):

    def __init__(self, api_address: str, parameters: Dict[str, Any]):
        super().__init__(api_address=api_address)
        try:
            self.api_key = parameters.pop('api_key')
            self.format = parameters.pop('format')
            self.id = parameters.pop('channel_id')
            self.opt_param = parameters
        except KeyError as ke:
            raise SystemExit(
                f"{EXCEPTION_HEADER} {ThingspeakURLBuilder.__name__} bad 'api.json' file structure => missing key={ke!s}"
            )

    def url(self) -> str:
        url = self.api_address + '/' + self.id + '/'
        url += 'feeds.' + self.format + QU
        url += 'api_key' + EQ + self.api_key + AND
        for param_name, param_value in self.opt_param.items():
            url += param_name + EQ + param_value + AND
        return url.strip(AND)
