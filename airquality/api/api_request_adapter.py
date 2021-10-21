#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 08:09
# @Description: this script defines the classes for connecting to the sensor's APIs and fetching the data.
#
#################################################
import builtins
from abc import ABC, abstractmethod
import urllib.request as req


class APIRequestAdapter(ABC):
    """Abstract Base Class for making API requests/fetching data from api.

    The __init__() method takes only the API address as argument."""

    def __init__(self):
        self.__api_address = None

    @property
    def api_address(self):
        return self.__api_address

    @api_address.setter
    def api_address(self, value: str):
        self.__api_address = value

    @abstractmethod
    def fetch(self, query_string: str) -> str:
        """Abstract method that defines the common interface for fetching data from API."""
        pass


class AtmotubeAPIRequestAdapter(APIRequestAdapter):
    """Class that wraps the Atmotube API request."""


    def __init__(self):
        super().__init__()


    def fetch(self, query_string: str) -> str:
        """This method takes the URL query string as argument and concatenate it with the 'api_address' instance
        variable: the result if a valid URL.

        In case of request failure, SystemExit exception is raised."""

        url = self.api_address + '?' + query_string
        try:
            response = req.urlopen(url)
        except Exception as err:
            raise SystemExit(f"{AtmotubeAPIRequestAdapter.__name__}: {str(err)}")
        finally:
            req.urlcleanup()
        return response


################################ FACTORY ################################
class APIRequestAdapterFactory(builtins.object):
    """Factory abstract base class for API request adapter objects."""

    @staticmethod
    def create_api_request_adapter(bot_personality: str) -> APIRequestAdapter:

        if bot_personality == "atmotube":
            return AtmotubeAPIRequestAdapter()
        else:
            raise SystemExit(f"{APIRequestAdapterFactory.__name__}: invalid bot personality {bot_personality}.")



