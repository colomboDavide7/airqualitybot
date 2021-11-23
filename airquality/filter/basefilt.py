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
import airquality.adapter.api2db.baseadpt as baseadpt


################################ SENSOR DATA FILTER BASE CLASS ################################
class BaseFilter(log.Loggable):

    def __init__(self, log_filename="log"):
        super(BaseFilter, self).__init__(log_filename=log_filename)

    @abc.abstractmethod
    def filter(self, to_filter: List[baseadpt.BaseUniformModel]) -> List[baseadpt.BaseUniformModel]:
        pass
