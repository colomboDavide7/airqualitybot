######################################################
#
# Author: Davide Colombo
# Date: 15/11/21 14:14
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
import airquality.logger.util.log as log


class Loggable(abc.ABC):

    def __init__(self, log_filename="log"):
        self.log_filename = log_filename
        self.file_logger = None
        self.console_logger = None

    def set_file_logger(self, logger: log.logging.Logger):
        self.file_logger = logger

    def set_console_logger(self, logger: log.logging.Logger):
        self.console_logger = logger

    def log_info(self, msg_to_log: str):
        if self.file_logger:
            self.file_logger.name(msg_to_log)

        if self.console_logger:
            self.console_logger.name(msg_to_log)

    def log_warning(self, msg_to_log: str):
        if self.file_logger:
            self.file_logger.warning(msg_to_log)

        if self.console_logger:
            self.console_logger.warning(msg_to_log)
