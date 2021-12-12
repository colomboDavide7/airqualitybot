######################################################
#
# Author: Davide Colombo
# Date: 14/11/21 19:43
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import List
import airquality.logger.loggable as log
import airquality.api.resp.abc as resptype


class FilterABC(log.Loggable, abc.ABC):

    def __init__(self, log_filename="log"):
        super(FilterABC, self).__init__(log_filename=log_filename)

    @abc.abstractmethod
    def filter(self, all_resp: List[resptype.APIRespTypeABC]) -> List[resptype.APIRespTypeABC]:
        pass
