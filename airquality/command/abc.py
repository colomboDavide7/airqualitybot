######################################################
#
# Author: Davide Colombo
# Date: 21/11/21 12:03
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
import airquality.logger.loggable as log


class CommandABC(log.Loggable, abc.ABC):

    @abc.abstractmethod
    def execute(self):
        pass
