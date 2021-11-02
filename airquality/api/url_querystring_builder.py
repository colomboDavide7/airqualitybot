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
from airquality.constants.shared_constants import EMPTY_DICT, PURPLEAIR_FIELDS_PARAM, \
    ATMOTUBE_MAC_PARAM, ATMOTUBE_API_KEY_PARAM, ATMOTUBE_DATE_PARAM

KEY_VAL_SEPARATOR = "="
CONCAT_SEPARATOR = "&"


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
            - date:     the date from which fetching data (format: 'YYYY-mm-dd')

        Optional parameters are:
            - order:    the order in which data are fetched (asc | desc)

        See: https://app.swaggerhub.com/apis/Atmotube/cloud_api/1.1#/AtmotubeDataItem."""

        querystring = ""
        if parameters == EMPTY_DICT:
            raise SystemExit(f"{URLQuerystringBuilderAtmotube.__name__}: empty API parameters.")

        keys = parameters.keys()

        # raise SystemExit if any mandated key is missing
        if ATMOTUBE_API_KEY_PARAM not in keys or ATMOTUBE_MAC_PARAM not in keys or ATMOTUBE_DATE_PARAM not in keys:
            raise SystemExit(f"{URLQuerystringBuilderAtmotube.__name__}: missing required parameters. "
                             f"Please, check the 'api_param' database table.")

        querystring += ATMOTUBE_API_KEY_PARAM + KEY_VAL_SEPARATOR + parameters[ATMOTUBE_API_KEY_PARAM] + CONCAT_SEPARATOR
        querystring += ATMOTUBE_MAC_PARAM + KEY_VAL_SEPARATOR + parameters[ATMOTUBE_MAC_PARAM] + CONCAT_SEPARATOR
        querystring += ATMOTUBE_DATE_PARAM + KEY_VAL_SEPARATOR + parameters[ATMOTUBE_DATE_PARAM] + CONCAT_SEPARATOR

        # Concatenate optional parameters (if any)
        for key in keys:
            if key not in (ATMOTUBE_API_KEY_PARAM, ATMOTUBE_MAC_PARAM, ATMOTUBE_DATE_PARAM):
                querystring += key + KEY_VAL_SEPARATOR + parameters[key] + CONCAT_SEPARATOR

        # Remove trailing '&'
        querystring = querystring.strip(CONCAT_SEPARATOR)
        return querystring


class URLQuerystringBuilderPurpleair(URLQuerystringBuilder):

    def make_querystring(self, parameters: Dict[str, Any]) -> str:
        """This method defines the rules for building purpleair URL querystring for fetching data from API.

        Required parameters are:
            - api_key:  private purple air api key
            - fields:   a list of comma separated values

        See: https://api.purpleair.com/#api-welcome-using-api-keys."""

        querystring = ""
        keys = parameters.keys()

        if parameters != EMPTY_DICT:

            if 'api_key' not in keys or PURPLEAIR_FIELDS_PARAM not in keys:
                raise SystemExit(f"{URLQuerystringBuilderPurpleair.__name__}: missing 'api_key' or 'fields' keys.")

            querystring += 'api_key' + KEY_VAL_SEPARATOR + parameters['api_key'] + CONCAT_SEPARATOR
            querystring += PURPLEAIR_FIELDS_PARAM + KEY_VAL_SEPARATOR
            for field in parameters[PURPLEAIR_FIELDS_PARAM]:
                querystring += field + ','
            querystring = querystring.strip(',') + CONCAT_SEPARATOR

            for key in keys:
                if key not in ('api_address', 'api_key', 'fields'):
                    querystring += key + KEY_VAL_SEPARATOR + parameters[key] + CONCAT_SEPARATOR
            querystring = querystring.strip(CONCAT_SEPARATOR)
        return querystring


class URLQuerystringBuilderThingspeak(URLQuerystringBuilder):

    def make_querystring(self, parameters: Dict[str, Any]) -> str:
        """This method defines the rules for building thingspeak URL querystring for fetching data from API.

        Required parameters are:
            - api_key:  private purple air api key
            - start:    starting timestamp
            - end:      end timestamp

        See: https://ch.mathworks.com/help/thingspeak/readdata.html."""

        querystring = ""
        keys = parameters.keys()

        if parameters != EMPTY_DICT:

            if 'api_key' not in keys or 'start' not in keys or 'end' not in keys:
                raise SystemExit(
                    f"{URLQuerystringBuilderThingspeak.__name__}: missing 'api_key' or 'start' or 'end' keys.")

            querystring += 'api_key' + KEY_VAL_SEPARATOR + parameters['api_key'] + CONCAT_SEPARATOR
            querystring += 'start' + KEY_VAL_SEPARATOR + parameters['start'] + CONCAT_SEPARATOR
            querystring += 'end' + KEY_VAL_SEPARATOR + parameters['end']

            querystring = querystring.replace(" ", "%20")
        return querystring


################################ FACTORY ################################
class URLQuerystringBuilderFactory(builtins.object):

    @classmethod
    def create_querystring_builder(cls, bot_personality: str) -> URLQuerystringBuilder:
        """Simple factory method that returns a specific instance of URLQuerystringBuilder based on
        'bot_personality' argument."""

        if bot_personality == "atmotube":
            return URLQuerystringBuilderAtmotube()
        elif bot_personality == "purpleair":
            return URLQuerystringBuilderPurpleair()
        elif bot_personality == "thingspeak":
            return URLQuerystringBuilderThingspeak()
        else:
            raise SystemExit(
                f"{URLQuerystringBuilderFactory.__name__}: cannot instantiate {URLQuerystringBuilder.__name__} "
                f"instance for personality='{bot_personality}'.")
