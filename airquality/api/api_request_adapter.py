#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 08:09
# @Description: This script contains the classes for connecting with the
#               sensors API for fetching the data.
#
#################################################

from abc import ABC, abstractmethod
import urllib.request as req


class APIRequestAdapter(ABC):
    """Abstract Base Class for making API requests/fetching data from api.

    The __init__() method takes only the API address as argument."""

    def __init__(self, api_address: str):
        self.__api_address = api_address

    @property
    def api_address(self):
        return self.__api_address

    @abstractmethod
    def fetch(self, query_string: str) -> str:
        """
        Abstract method that defines the common interface through which
        a subclass can fetch data from API.

        Return the response string from the API."""
        pass


class AtmotubeAPIRequestAdapter(APIRequestAdapter):
    """Class that wraps the Atmotube API request."""


    def fetch(self, query_string: str) -> str:
        """
        This method takes the URL query string as argument and concatenate it
        with the 'api_address' instance variable: the result if a valid URL.

        In case of failure of the request, SystemExit exception is raised."""

        url = self.api_address + '?' + query_string
        try:
            response = req.urlopen(url)
        except Exception as err:
            raise SystemExit(f"{AtmotubeAPIRequestAdapter.__name__}: {str(err)}")
        finally:
            req.urlcleanup()
        return response


################################ FACTORY ################################
class APIRequestAdapterFactory(ABC):
    """Factory abstract base class for API request adapter objects."""

    @abstractmethod
    def create_api_request_adapter(self, api_address: str) -> APIRequestAdapter:
        """Abstract method for creating API request adapter objects."""
        pass

class AtmotubeAPIRequestAdapterFactory(APIRequestAdapterFactory):
    """Factory concrete class specific for creating atmotube API request adapters."""

    def create_api_request_adapter(self, api_address: str) -> AtmotubeAPIRequestAdapter:
        """Return AtmotubeAPIRequestAdapter instance."""
        return AtmotubeAPIRequestAdapter(api_address)
