#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 09:52
# @Description: this script defines a class for building valid URL querystring based on sensor type.
#
#################################################
import builtins
from typing import Dict, Any
from abc import ABC, abstractmethod
from airquality.constants.shared_constants import ATMOTUBE_API_PARAMETERS


KEY_VAL_SEPARATOR = "="
CONCAT_SEPARATOR  = "&"


class URLQuerystringBuilder(ABC):
    """Abstract Base Class for building URL querystring dynamically from a set of parameters."""

    @abstractmethod
    def make_querystring(self, parameters: Dict[str, Any]) -> str:
        pass


class URLQuerystringBuilderAtmotube(URLQuerystringBuilder):

    def make_querystring(self, parameters: Dict[str, Any]) -> str:
        """This method defines the rules for building a valid Atmotube querystring for fetching data from API.

        Required parameters are:
            - api_key:  the user's private api key
            - mac:      the sensor's mac address
            - date:     the date from which fetching data

        Optional parameters are:
            - order:    the order in which data are fetched (asc | desc)

        See: https://app.swaggerhub.com/apis/Atmotube/cloud_api/1.1#/AtmotubeDataItem."""

        querystring = ""
        status_check = 0b000

        if parameters:
            for key, val in parameters.items():
                if key in ATMOTUBE_API_PARAMETERS:
                    querystring += key + KEY_VAL_SEPARATOR + val + CONCAT_SEPARATOR
                else:
                    print(f"{URLQuerystringBuilder.make_querystring.__name__}: ignore invalid argument '{key}'.")

                if key == 'api_key':
                    status_check |= 0b001
                elif key == 'mac':
                    status_check |= 0b010
                elif key == 'date':
                    status_check |= 0b100

        if status_check != 0b111:
            raise SystemExit(f"{URLQuerystringBuilder.make_querystring.__name__}: missing required arguments.")

        querystring = querystring.strip(CONCAT_SEPARATOR)
        return querystring



class URLQuerystringBuilderPurpleair(URLQuerystringBuilder):


    def make_querystring(self, parameters: Dict[str, Any]) -> str:
        """This method defines the rules for building purple air URL querystring for fetching data from API.

        Required parameters are:
            - api_key:  private purple air api key
            - fields:   a list of comma separated values

        See: https://api.purpleair.com/#api-welcome-using-api-keys."""

        querystring = ""
        api_key_missing = True
        fields_missing = True

        if parameters:
            for key, val in parameters.items():
                if key == "api_key":
                    querystring += key + KEY_VAL_SEPARATOR + val + CONCAT_SEPARATOR
                    api_key_missing = False
                elif key == "fields":
                    querystring += key + KEY_VAL_SEPARATOR
                    if not isinstance(val, list):
                        raise SystemExit(f"{URLQuerystringBuilder.make_querystring.__name__}:"
                                         f"'fields' value is required to be a list")
                    for f in val:
                        querystring += f + ","
                    querystring = querystring.strip(',')
                    querystring += CONCAT_SEPARATOR
                    fields_missing = False
                else:
                    querystring += key + KEY_VAL_SEPARATOR + val + CONCAT_SEPARATOR

            querystring = querystring.strip(CONCAT_SEPARATOR)

        if api_key_missing or fields_missing:
            raise SystemExit(f"{URLQuerystringBuilder.make_querystring.__name__}: missing field error."
                             f"Please, check your 'properties/setup.json'")

        return querystring




################################ FACTORY ################################
class URLQuerystringBuilderFactory(builtins.object):

    @staticmethod
    def create_querystring_builder(bot_personality: str) -> URLQuerystringBuilder:
        """Simple factory method that returns a specific instance of URLQuerystringBuilder based on
        'bot_personality'."""

        if bot_personality == "atmotube":
            return URLQuerystringBuilderAtmotube()
        elif bot_personality == "purpleair":
            return URLQuerystringBuilderPurpleair()
