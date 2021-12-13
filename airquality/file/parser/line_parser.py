######################################################
#
# Author: Davide Colombo
# Date: 10/12/21 16:28
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Generator, List
import airquality.file.parser.abc as parserabc


class TSVLineParser(parserabc.FileParserABC):

    def parse(self, text: str) -> Generator[List[str], None, None]:
        lines = text.split('\n')
        self.log_info(f"{self.__class__.__name__} found #{len(lines)} lines")
        for line in lines:
            if line:
                yield line.split('\t')
