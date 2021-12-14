######################################################
#
# Author: Davide Colombo
# Date: 12/12/21 19:31
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.command.abc as cmdabc
import airquality.api.api_repo as apirepo
import airquality.file.parser.abc as parser
import airquality.api.resp.abc as builder
import airquality.filter.abc as filterabc
import airquality.database.sql.abc as sqltype


# ------------------------------- SensorCommand ------------------------------- #
class SensorCommand(cmdabc.CommandABC):

    def __init__(
            self,
            api_repo: apirepo.APIRepo,
            resp_parser: parser.FileParserABC,
            resp_builder: builder.APIRespBuilderABC,
            resp_filter: filterabc.FilterABC,
            db_repo: sqltype.DBRepoABC
    ):
        super(SensorCommand, self).__init__()
        self.api_repo = api_repo
        self.resp_parser = resp_parser
        self.resp_builder = resp_builder
        self.resp_filter = resp_filter
        self.db_repo = db_repo

    ################################ execute() ################################
    def execute(self):
        api_responses = self.api_repo.read_all()
        for resp in api_responses:
            parsed_resp = self.resp_parser.parse(resp)
            all_responses = self.resp_builder.build(parsed_resp)
            if not all_responses:
                self.log_info(f"{self.__class__.__name__} empty API responses")
                continue

            filtered_responses = self.resp_filter.filter(all_responses)
            if not filtered_responses:
                self.log_info(f"{self.__class__.__name__} all measurements are already present into the database")
                continue

            self.db_repo.push(filtered_responses)
