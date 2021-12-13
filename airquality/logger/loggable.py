######################################################
#
# Author: Davide Colombo
# Date: 15/11/21 14:14
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
import airquality.logger.fact as log


# ------------------------------- LoggableABC ------------------------------- #
class LoggableABC(abc.ABC):

    def __init__(self):
        self._file_logger = None
        self._console_logger = None

    ################################ set_file_logger() ###############################
    def set_file_logger(self, logger: log.logging.Logger):
        self._file_logger = logger

    ################################ set_console_logger() ###############################
    def set_console_logger(self, logger: log.logging.Logger):
        self._console_logger = logger

    ################################ log_info() ###############################
    def log_info(self, msg_to_log: str):
        if self._file_logger:
            self._file_logger.info(msg_to_log)
        if self._console_logger:
            self._console_logger.info(msg_to_log)

    ################################ log_warning() ###############################
    def log_warning(self, msg_to_log: str):
        if self._file_logger:
            self._file_logger.warning(msg_to_log)
        if self._console_logger:
            self._console_logger.warning(msg_to_log)
