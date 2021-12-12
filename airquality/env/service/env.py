######################################################
#
# Author: Davide Colombo
# Date: 09/12/21 16:52
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import sys
import airquality.env.abc as envabc
import airquality.logger.util.log as log
import airquality.file.repo.abc as filerepo
import airquality.file.line.abc as filebuilder
import airquality.file.parser.abc as fileparser
import airquality.database.repo.abc as dbrepo
import airquality.filter.geonames as filefilter


class ServiceEnv(envabc.EnvironmentABC):

    def __init__(
            self,
            file_logger: log.logging.Logger,
            console_logger: log.logging.Logger,
            error_logger: log.logging.Logger,
            file_repo: filerepo.FileRepoABC,
            file_parser: fileparser.FileParserABC,
            file_builder: filebuilder.LineBuilderABC,
            file_filter: filefilter.GeonamesFilter,
            db_repo: dbrepo.DatabaseRepoABC
    ):
        super(ServiceEnv, self).__init__(file_logger=file_logger, console_logger=console_logger, error_logger=error_logger)
        self.file_repo = file_repo
        self.file_parser = file_parser
        self.file_builder = file_builder
        self.file_filter = file_filter
        self.db_repo = db_repo

    def run(self):
        try:
            file_contents = self.file_repo.read_all()
            for fc in file_contents:
                parsed_lines = self.file_parser.parse(fc)
                all_lines = self.file_builder.build(parsed_lines)
                filtered_lines = self.file_filter.filter(all_lines)
                self.db_repo.push(filtered_lines)
        except SystemExit as err:
            err_msg = f"{self.__class__.__name__} catches {err.__class__.__name__} exception => {err!r}"
            self.file_logger.exception(err_msg)
            self.error_logger.exception(err_msg)
            sys.exit(1)
        finally:
            self.shutdown()

    def shutdown(self):
        log.logging.shutdown()

        # TODO: shutdown database connection

        # TODO: shutdown file connections (if any)
