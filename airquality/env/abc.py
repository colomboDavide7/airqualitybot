######################################################
#
# Author: Davide Colombo
# Date: 09/12/21 16:51
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
import airquality.logger.util.log as log


class EnvironmentABC(abc.ABC):

    def __init__(self, file_logger: log.logging.Logger, console_logger: log.logging.Logger, error_logger: log.logging.Logger):
        self.file_logger = file_logger
        self.console_logger = console_logger
        self.error_logger = error_logger

    @abc.abstractmethod
    def run(self):
        pass

    @abc.abstractmethod
    def shutdown(self):
        pass
