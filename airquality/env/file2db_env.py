######################################################
#
# Author: Davide Colombo
# Date: 09/12/21 16:52
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.env.env_abc as baseenv
import airquality.logger.util.log as log
import airquality.source.file as filesource
import airquality.database.repo.repo as dbrepo


class FileToDatabaseEnvironment(baseenv.EnvironmentABC):

    def __init__(
            self,
            file_logger: log.logging.Logger,
            console_logger: log.logging.Logger,
            error_logger: log.logging.Logger,
            source: filesource.FileSourceABC,
            target: dbrepo.DatabaseRepoABC
    ):
        super(FileToDatabaseEnvironment, self).__init__(file_logger=file_logger, console_logger=console_logger, error_logger=error_logger)
        self.source = source
        self.target = target

    def get_from_source(self):
        pass

    def push_to_target(self):
        pass

    def shutdown(self):
        pass
