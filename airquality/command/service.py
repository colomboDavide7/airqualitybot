######################################################
#
# Author: Davide Colombo
# Date: 03/12/21 16:18
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.command.abc as cmdabc
import airquality.filter.abc as filterabc
import airquality.file.repo.abc as filerepo
import airquality.file.parser.abc as parser
import airquality.file.line.abc as builder
import airquality.database.sql.abc as sqltype


# ------------------------------- ServiceCommand ------------------------------- #
class ServiceCommand(cmdabc.CommandABC):

    def __init__(
            self,
            filename: str,
            file_repo: filerepo.FileRepoABC,
            file_parser: parser.FileParserABC,
            line_builder: builder.LineBuilderABC,
            file_filter: filterabc.FilterABC,
            db_repo: sqltype.DBRepoABC
    ):
        super(ServiceCommand, self).__init__()
        self.filename = filename
        self.file_repo = file_repo
        self.file_parser = file_parser
        self.line_builder = line_builder
        self.file_filter = file_filter
        self.db_repo = db_repo

    ################################ execute() ################################
    def execute(self):
        file_content = self.file_repo.read_file(self.filename)
        parsed_content = self.file_parser.parse(file_content)
        all_lines = self.line_builder.build(parsed_content)
        filtered_lines = self.file_filter.filter(all_lines)
        self.db_repo.push(filtered_lines)
