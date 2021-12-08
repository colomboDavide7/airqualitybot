######################################################
#
# Author: Davide Colombo
# Date: 14/11/21 19:43
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
import airquality.logger.loggable as log


class FilterABC(log.Loggable, abc.ABC):

    def __init__(self, log_filename="log"):
        super(FilterABC, self).__init__(log_filename=log_filename)

    @abc.abstractmethod
    def filter(self, resp2filter):
        pass
