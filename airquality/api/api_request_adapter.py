#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 08:09
# @Description: this script defines the classes for connecting to the sensor's APIs and fetching the data.
#
#################################################
import builtins
import urllib.request as req


class APIRequestAdapter(builtins.object):


    def __init__(self, api_address):
        self.__api_address = api_address

    def fetch(self, querystring: str) -> str:
        """This method takes the URL query string as argument and concatenate it with the 'api_address' instance
        variable: the result if a valid URL.

        In case of request failure, SystemExit exception is raised."""

        url = self.__api_address + '?' + querystring
        try:
            answer = req.urlopen(url).read()
        except Exception as err:
            raise SystemExit(f"{APIRequestAdapter.__name__}: {str(err)}")
        finally:
            req.urlcleanup()
        return answer
