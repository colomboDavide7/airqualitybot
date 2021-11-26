######################################################
#
# Author: Davide Colombo
# Date: 14/11/21 19:43
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import List, Union
import airquality.logger.loggable as log
import airquality.types.apiresp.measresp as measresp
import airquality.types.apiresp.inforesp as inforesp

RETURNED_TYPE = Union[measresp.MeasureAPIResp, inforesp.SensorInfoResponse]


################################ FILTER BASE CLASS ################################
class BaseFilter(log.Loggable):

    def __init__(self, log_filename="log"):
        super(BaseFilter, self).__init__(log_filename=log_filename)

    @abc.abstractmethod
    def filter(self, resp2filter: List[RETURNED_TYPE]) -> List[RETURNED_TYPE]:
        pass
