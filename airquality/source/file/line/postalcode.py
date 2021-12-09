######################################################
#
# Author: Davide Colombo
# Date: 09/12/21 17:20
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Generator, List
import airquality.source.file.line.abc as lineabc


# ------------------------------- PostalcodeLineType ------------------------------- #
class PostalcodeLineType(lineabc.LineTypeABC):

    def __init__(self, postal_code: str):
        self.postal_code = postal_code


# ------------------------------- PostalcodeLineBuilder ------------------------------- #
class PostalcodeLineBuilder(lineabc.LineBuilderABC):

    def __init__(self, log_filename="log"):
        super(PostalcodeLineBuilder, self).__init__(log_filename=log_filename)

    ################################ build_lines() ################################
    def build_lines(self, parsed_lines: Generator[List[str],  None, None]) -> Generator[PostalcodeLineType, None, None]:
        for line in parsed_lines:
            yield PostalcodeLineType(postal_code=line[0])
