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

    def __init__(self):
        self.logger = None
        self.debugger = None
        self.info_messages = []
        self.warning_messages = []

    def set_logger(self, logger: log.logging.Logger):
        self.logger = logger

    def set_debugger(self, debugger: log.logging.Logger):
        self.debugger = debugger

    def log_messages(self):
        if self.logger:
            for msg in self.info_messages:
                self.logger.info(msg)
            for msg in self.warning_messages:
                self.logger.warning(msg)

        if self.debugger:
            for msg in self.info_messages:
                self.debugger.info(msg)
            for msg in self.warning_messages:
                self.debugger.warning(msg)

        self._clear_messages()

    def _clear_messages(self):
        self.info_messages.clear()
        self.warning_messages.clear()
