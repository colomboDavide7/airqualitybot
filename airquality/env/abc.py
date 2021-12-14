######################################################
#
# Author: Davide Colombo
# Date: 09/12/21 16:51
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
import airquality.logger.fact as log
import airquality.database.conn as db


# ------------------------------- EnvironmentABC ------------------------------- #
class EnvironmentABC(abc.ABC):

    def __init__(self, file_logger: log.logging.Logger, console_logger: log.logging.Logger, error_logger: log.logging.Logger):
        self.file_logger = file_logger
        self.console_logger = console_logger
        self.error_logger = error_logger

    @abc.abstractmethod
    def run(self):
        pass

    ################################ shutdown() ################################
    def shutdown(self):
        msg = f"{self.__class__.__name__} in {self.shutdown.__name__}: status = success"
        self.file_logger.info(msg)
        self.console_logger.info(msg)
        log.shutdown()
        db.shutdown()
