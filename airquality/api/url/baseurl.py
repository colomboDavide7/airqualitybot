######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 16:36
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import Dict, Any
import airquality.logger.loggable as log


class BaseURL(log.Loggable, abc.ABC):

    def __init__(self, address: str, parameters: Dict[str, Any], log_filename="log"):
        super(BaseURL, self).__init__(log_filename=log_filename)
        self.address = address
        self.parameters = parameters

    @abc.abstractmethod
    def url(self) -> str:
        pass

    @abc.abstractmethod
    def _exit_on_bad_url_parameters(self):
        pass

    def _get_querystring(self):
        return '&'.join(f"{n}={v}" for n, v in self.parameters.items())
