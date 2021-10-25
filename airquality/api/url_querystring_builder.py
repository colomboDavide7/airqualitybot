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

KEY_VAL_SEPARATOR = "="
CONCAT_SEPARATOR = "&"


class URLQuerystringBuilder(ABC):

    @abstractmethod
    def make_querystring(self, parameters: Dict[str, Any]) -> str:
        pass


    """Class that defines @staticmethods for building the URL querystring based on sensor type"""

    @staticmethod
    def AT_querystring_from_date(api_param: Dict[str, Any]) -> str:
        """Static method that builds a URL querystring for the Atmotube sensor using 'date' field.

        -querystring:   the variable that holds the querystring
        -status_check:  binary variable used to check if all mandated parameters are provided

        If 'api_key', 'mac' or 'date' parameters missed, SystemExit exception is raised."""

        querystring = ""
        status_check = 0b000

        if api_param:
            for key, val in api_param.items():
                if key in ('api_key', 'mac', 'date', 'order'):
                    querystring += key + KEY_VAL_SEPARATOR + val + CONCAT_SEPARATOR
                else:
                    print(f"{URLQuerystringBuilder.__name__}: ignore invalid argument '{key}' in method "
                          f"'{URLQuerystringBuilder.AT_querystring_from_date.__name__}()'.")

                if key == 'api_key':
                    status_check |= 0b001
                elif key == 'mac':
                    status_check |= 0b010
                elif key == 'date':
                    status_check |= 0b100

        if status_check != 0b111:
            raise SystemExit(f"{URLQuerystringBuilder.__name__}: missing required arguments in method "
                             f"'{URLQuerystringBuilder.AT_querystring_from_date.__name__}()'.")

        querystring = querystring.strip(CONCAT_SEPARATOR)
        return querystring


    @staticmethod
    def PA_querystring_from_fields(api_param: Dict[str, Any]):
        """Static method that takes PurpleAir sensor's API parameters and builds a URL querystring from those."""

        querystring = ""
        api_key_missing = True
        fields_missing = True

        if api_param:
            for key, val in api_param.items():
                if key == "api_key":
                    querystring += key + KEY_VAL_SEPARATOR + val + CONCAT_SEPARATOR
                    api_key_missing = False
                elif key == "fields":
                    querystring += key + KEY_VAL_SEPARATOR
                    if not isinstance(val, list):
                        raise SystemExit(f"{URLQuerystringBuilder.PA_querystring_from_fields.__name__}:"
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
            raise SystemExit(f"{URLQuerystringBuilder.PA_querystring_from_fields.__name__}: missing field error."
                             f"Please, check your 'properties/setup.json'")

        return querystring


class URLQuerystringBuilderAtmotube(URLQuerystringBuilder):

    def make_querystring(self, parameters: Dict[str, Any]) -> str:

        querystring = ""
        status_check = 0b000

        if parameters:
            for key, val in parameters.items():
                if key in ('api_key', 'mac', 'date', 'order'):
                    querystring += key + KEY_VAL_SEPARATOR + val + CONCAT_SEPARATOR
                else:
                    print(f"{URLQuerystringBuilder.__name__}: ignore invalid argument '{key}' in method "
                          f"'{URLQuerystringBuilder.AT_querystring_from_date.__name__}()'.")

                if key == 'api_key':
                    status_check |= 0b001
                elif key == 'mac':
                    status_check |= 0b010
                elif key == 'date':
                    status_check |= 0b100

        if status_check != 0b111:
            raise SystemExit(f"{URLQuerystringBuilder.__name__}: missing required arguments in method "
                             f"'{URLQuerystringBuilder.AT_querystring_from_date.__name__}()'.")

        querystring = querystring.strip(CONCAT_SEPARATOR)
        return querystring


class URLQuerystringBuilderPurpleair(URLQuerystringBuilder):

    def make_querystring(self, parameters: Dict[str, Any]) -> str:
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
                        raise SystemExit(f"{URLQuerystringBuilder.PA_querystring_from_fields.__name__}:"
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
            raise SystemExit(f"{URLQuerystringBuilder.PA_querystring_from_fields.__name__}: missing field error."
                             f"Please, check your 'properties/setup.json'")

        return querystring




################################ FACTORY ################################
class URLQuerystringBuilderFactory(builtins.object):

    @staticmethod
    def create_querystring_builder(bot_personality: str) -> URLQuerystringBuilder:
        if bot_personality == "atmotube":
            return URLQuerystringBuilderAtmotube()
        elif bot_personality == "purpleair":
            return URLQuerystringBuilderPurpleair()
        else:
            raise SystemExit(f"{URLQuerystringBuilderFactory.create_querystring_builder.__name__}:"
                             f"invalid bot personality '{bot_personality}'.")
