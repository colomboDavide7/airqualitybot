######################################################
#
# Author: Davide Colombo
# Date: 10/12/21 10:50
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from urllib.request import urlopen
from urllib.error import URLError
import airquality.logger.loggable as log


class APIRequest(log.Loggable):

    def __init__(self, log_filename="log"):
        super(APIRequest, self).__init__(log_filename=log_filename)

    def fetch_from_url(self, url: str) -> str:
        try:
            return urlopen(url).read()
        except URLError as err:
            msg = f"{self.__class__.__name__} catches {err.__class__.__name__} exception => {err!r}"
            self.log_exception(msg)
            raise SystemExit(msg)
        except ValueError as verr:
            msg = f"{self.__class__.__name__} catches a {verr.__class__.__name__} error => {verr!r}"
            self.log_exception(msg)
            raise SystemExit(msg)
