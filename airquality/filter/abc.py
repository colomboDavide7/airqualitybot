######################################################
#
# Author: Davide Colombo
# Date: 14/11/21 19:43
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
import airquality.logger.loggable as log


class FilterABC(log.LoggableABC, abc.ABC):

    @abc.abstractmethod
    def filter(self, all_resp):
        pass
