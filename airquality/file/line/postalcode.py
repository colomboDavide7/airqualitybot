######################################################
#
# Author: Davide Colombo
# Date: 09/12/21 17:20
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Generator, List
import airquality.file.line.abc as lineabc


# ------------------------------- PostalcodeLineType ------------------------------- #
class PostalcodeLineType(lineabc.LineTypeABC):

    def __init__(self, postal_code: str):
        self.postal_code = postal_code


# ------------------------------- PostalcodeLineBuilder ------------------------------- #
class PostalcodeLineBuilder(lineabc.LineBuilderABC):

    ################################ build() ################################
    def build(self, parsed_lines: Generator[List[str], None, None]) -> Generator[PostalcodeLineType, None, None]:
        try:
            for line in parsed_lines:
                yield PostalcodeLineType(postal_code=line[0])
        except IndexError as err:
            raise SystemExit(f"{self.__class__.__name__} catches {err.__class__.__name__} in {self.build.__name__} => {err!r}")
