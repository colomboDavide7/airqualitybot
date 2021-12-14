######################################################
#
# Author: Davide Colombo
# Date: 13/12/21 15:30
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import sys
from typing import List
import airquality.env.abc as envabc
import airquality.logger.fact as log
import airquality.command.abc as cmdtype


# ------------------------------- Environment ------------------------------- #
class Environment(envabc.EnvironmentABC):

    def __init__(
            self, file_logger: log.LOG_TYPE, console_logger: log.LOG_TYPE, error_logger: log.LOG_TYPE, commands: List[cmdtype.CommandABC]
    ):
        super(Environment, self).__init__(file_logger=file_logger, console_logger=console_logger, error_logger=error_logger)
        self.commands = commands

    ################################ run() ################################
    def run(self):
        try:
            for cmd in self.commands:
                cmd.execute()
        except SystemExit as err:
            self.error_logger.exception(str(err))
            self.console_logger.exception(str(err))
            sys.exit(1)
        finally:
            super().shutdown()
