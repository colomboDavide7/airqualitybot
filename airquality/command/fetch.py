######################################################
#
# Author: Davide Colombo
# Date: 21/11/21 17:49
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.command.abc as cmdtype
import airquality.filter.abc as filtertype
import airquality.api.api_repo as apirepo
import airquality.file.parser.abc as parser
import airquality.api.resp.abc as builder
import airquality.database.exe.abc as exetype


# ------------------------------- FetchCommand ------------------------------- #
class FetchCommand(cmdtype.CommandABC):

    def __init__(
            self,
            api_repo: apirepo.APIRepo,
            resp_parser: parser.FileParserABC,
            resp_builder: builder.APIRespBuilderABC,
            resp_filter: filtertype.FilterABC,
            query_executor: exetype.QueryExecutorABC
    ):
        super(FetchCommand, self).__init__()
        self.api_repo = api_repo
        self.resp_parser = resp_parser
        self.resp_builder = resp_builder
        self.resp_filter = resp_filter
        self.query_executor = query_executor

    ################################ execute() ################################
    def execute(self):
        api_responses = self.api_repo.read_all()
        for resp in api_responses:
            parsed_responses = self.resp_parser.parse(resp)
            all_responses = self.resp_builder.build(parsed_responses)
            if not all_responses:
                self.log_info(f"{self.__class__.__name__} empty API responses")
                continue

            filtered_responses = self.resp_filter.filter(all_responses)
            if not filtered_responses:
                self.log_info(f"{self.__class__.__name__} all measurements are already present into the database")
                continue

            self.query_executor.execute(filtered_responses)
