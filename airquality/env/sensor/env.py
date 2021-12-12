######################################################
#
# Author: Davide Colombo
# Date: 11/12/21 17:24
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List
import airquality.env.abc as envabc
import airquality.logger.util.log as log
import airquality.database.conn.adapt as db
import airquality.command.abc as cmdtype


# ------------------------------- APIEnv ------------------------------- #
class APIEnv(envabc.EnvironmentABC):

    def __init__(
            self,
            file_logger: log.logging.Logger,
            console_logger: log.logging.Logger,
            error_logger: log.logging.Logger,
            commands: List[cmdtype.CommandABC]
    ):
        super(APIEnv, self).__init__(file_logger=file_logger, console_logger=console_logger, error_logger=error_logger)
        self.commands = commands

    ################################ run() ################################
    def run(self):
        try:
            for cmd in self.commands:
                cmd.execute()
        except SystemExit as err:
            self.error_logger.exception(str(err))
            self.console_logger.exception(str(err))
        finally:
            self.shutdown()

    ################################ shutdown() ################################
    def shutdown(self):
        log.logging.shutdown()
        db.shutdown()
