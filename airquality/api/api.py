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
    """Abstract Base Class for the APIRequest.

    The __init__() method takes only the api address as argument."""

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

        Returns the response string from the server."""
        pass


class AtmotubeAPIRequestAdapter(APIRequestAdapter):
    """Class that wraps the Atmotube API requests behaviour."""


    def fetch(self, query_string: str) -> str:
        """
        This method takes the URL query string as argument and concat it
        with the 'api_address' instance variable for building a valid URL.

        Then, it tries to open the URL.

        If any Exception will occur, SystemExit exception is raised."""

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
    """
    Abstract Base Class that defines the interface for all the concrete
    API Request Factory subclasses."""

    @abstractmethod
    def create_request(self, api_address: str) -> APIRequestAdapter:
        """Abstract method for creating the api request object."""
        pass

class AtmotubeAPIRequestAdapterFactory(APIRequestAdapterFactory):
    """
    Factory class specific for creating the Atmotube API Request instances.
    """

    def create_request(self, api_address: str) -> AtmotubeAPIRequestAdapter:
        """Create Atmotube API Request instance."""
        return AtmotubeAPIRequestAdapter(api_address)
