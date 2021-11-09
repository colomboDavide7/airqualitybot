#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 08:09
# @Description: this script defines an adapter class that wraps the 'urllib' module functionality for connecting
#               to sensor's API and fetch data.
#
#################################################
import urllib.request as req
from airquality.core.constants.shared_constants import EXCEPTION_HEADER


class UrllibAdapter:

    @staticmethod
    def fetch(url: str) -> str:
        try:
            answer = req.urlopen(url).read()
        except Exception as ex:
            raise SystemExit(f"{EXCEPTION_HEADER} {UrllibAdapter.__name__} bad url => {ex!s}")
        finally:
            req.urlcleanup()
        return answer
