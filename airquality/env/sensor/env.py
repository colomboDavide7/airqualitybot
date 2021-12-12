######################################################
#
# Author: Davide Colombo
# Date: 11/12/21 17:24
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.env.abc as envabc
import airquality.logger.util.log as log
import airquality.api.api_repo as apirepo
import airquality.file.parser.abc as parser
import airquality.api.resp.abc as builder
import airquality.filter.abc as flt
import airquality.database.record.abc as recabc
import airquality.database.repo.abc as dbrepo


class APIEnv(envabc.EnvironmentABC):

    def __init__(
            self,
            file_logger: log.logging.Logger,
            console_logger: log.logging.Logger,
            error_logger: log.logging.Logger,
            api_repo: apirepo.APIRepo,
            resp_parser: parser.FileParserABC,
            resp_builder: builder.APIRespBuilderABC,
            resp_filter: flt.FilterABC,
            rec_builder: recabc.RecordBuilderABC,
            db_repo: dbrepo.DatabaseRepoABC
    ):
        super(APIEnv, self).__init__(file_logger=file_logger, console_logger=console_logger, error_logger=error_logger)
        self.api_repo = api_repo
        self.resp_parser = resp_parser
        self.resp_builder = resp_builder
        self.resp_filter = resp_filter
        self.rec_builder = rec_builder
        self.db_repo = db_repo

    def run(self):
        try:
            api_responses = self.api_repo.read_all()
            for resp in api_responses:
                parsed_resp = self.resp_parser.parse(resp)

                all_resp = self.resp_builder.build(parsed_resp)
                if not all_resp:
                    msg = f"{self.__class__.__name__} empty API response"
                    self.file_logger.info(msg)
                    self.console_logger.info(msg)
                    return

                filtered_resp = self.resp_filter.filter(all_resp)
                if not filtered_resp:
                    msg = f"{self.__class__.__name__} all the sensors are already present into the database"
                    self.file_logger.info(msg)
                    self.console_logger.info(msg)
                    return

                records = self.rec_builder.build(filtered_resp)
                self.db_repo.push(records)
        except SystemExit as err:
            self.error_logger.exception(str(err))
            self.console_logger.exception(str(err))
        finally:
            self.shutdown()

    def shutdown(self):
        log.logging.shutdown()

        # TODO: shutdown database connection

        # TODO: shutdown file connections (if any)
