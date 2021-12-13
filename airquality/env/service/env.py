######################################################
#
# Author: Davide Colombo
# Date: 09/12/21 16:52
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import sys
from typing import List
import airquality.env.abc as envabc
import airquality.logger.util.log as log
import airquality.command.service as cmdtype

# import airquality.file.repo.abc as filerepo
# import airquality.file.line.abc as filebuilder
# import airquality.file.parser.abc as fileparser
# import airquality.database.repo.abc as dbrepo
# import airquality.filter.geoarea as filefilter


class ServiceEnv(envabc.EnvironmentABC):

    def __init__(
            self,
            file_logger: log.logging.Logger,
            console_logger: log.logging.Logger,
            error_logger: log.logging.Logger,
            commands: List[cmdtype.ServiceCommand]
            # file_repo: filerepo.FileRepoABC,
            # file_parser: fileparser.FileParserABC,
            # file_builder: filebuilder.LineBuilderABC,
            # file_filter: filefilter.GeoareaFilter,
            # db_repo: dbrepo.DatabaseRepoABC
    ):
        super(ServiceEnv, self).__init__(file_logger=file_logger, console_logger=console_logger, error_logger=error_logger)
        self.commands = commands
        # self.file_repo = file_repo
        # self.file_parser = file_parser
        # self.file_builder = file_builder
        # self.file_filter = file_filter
        # self.db_repo = db_repo

    ################################ run() ################################
    def run(self):
        try:
            for cmd in self.commands:
                cmd.execute()
            # file_contents = self.file_repo.read_all()
            # for fc in file_contents:
            #     parsed_lines = self.file_parser.parse(fc)
            #     all_lines = self.file_builder.build(parsed_lines)
            #     filtered_lines = self.file_filter.filter(all_lines)
        except SystemExit as err:
            self.console_logger.exception(str(err))
            self.error_logger.exception(str(err))
            sys.exit(1)
        finally:
            self.shutdown()

    ################################ shutdown() ################################
    def shutdown(self):
        log.logging.shutdown()

