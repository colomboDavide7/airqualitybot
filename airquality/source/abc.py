######################################################
#
# Author: Davide Colombo
# Date: 08/12/21 14:27
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
import airquality.logger.loggable as log


class SourceABC(log.Loggable, abc.ABC):

    def __init__(self, log_filename="log"):
        super(SourceABC, self).__init__(log_filename=log_filename)

    @abc.abstractmethod
    def get(self):
        pass
