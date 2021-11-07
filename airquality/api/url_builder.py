#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 09:52
# @Description: this script defines a simple factory class for building valid URL querystring based on sensor type.
#
#################################################
import builtins
from typing import Dict, Any
from abc import ABC, abstractmethod
from airquality.constants.shared_constants import EXCEPTION_HEADER


class URLBuilder(ABC):

    @abstractmethod
    def build_url(self, parameters: Dict[str, Any]) -> str:
        pass


class URLBuilderPurpleair(URLBuilder):

    def build_url(self, parameters: Dict[str, Any]) -> str:
        """This method defines the rules for building purpleair URL querystring for fetching data from API.

        Required parameters are:
            - api_key:  private purple air api key
            - fields:   a list of comma separated values

        See: https://api.purpleair.com/#api-welcome-using-api-keys."""

        if not parameters:
            raise SystemExit(f"{URLBuilderPurpleair.__name__}: empty API parameters.")

        keys = parameters.keys()

        # raise SystemExit if any mandated API param is missing
        if 'api_key' not in keys or 'fields' not in keys or 'api_address' not in keys:
            raise SystemExit(f"{EXCEPTION_HEADER} {URLBuilderPurpleair.__name__} misses ['api_address' | 'api_key' | "
                             f"'fields']. Please, check your 'api.json' local file.")

        # build the querystring
        querystring = parameters.pop('api_address') + '?'
        for key, val in parameters.items():
            if key == 'fields':
                querystring += key + '='
                for field in parameters[key]:
                    querystring += field + ','
                querystring = querystring.strip(',') + '&'
            else:
                querystring += key + '=' + val + '&'
        return querystring.strip('&')


################################ FACTORY ################################
class URLBuilderFactory(builtins.object):

    def __init__(self, url_builder_class=URLBuilder):
        self.url_builder_class = url_builder_class

    def create_url_builder(self) -> URLBuilder:
        return self.url_builder_class()
