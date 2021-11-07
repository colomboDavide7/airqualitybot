#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 08:09
# @Description: this script defines an adapter class that wraps the 'urllib' module functionality for connecting
#               to sensor's API and fetch data.
#
#################################################
import builtins
import urllib.request as req


class APIRequestAdapter(builtins.object):

    @staticmethod
    def fetch(url: str) -> str:
        try:
            answer = req.urlopen(url).read()
        except Exception as err:
            raise SystemExit(f"{APIRequestAdapter.__name__}: {str(err)}")
        finally:
            req.urlcleanup()
        return answer
