######################################################
#
# Author: Davide Colombo
# Date: 03/12/21 17:09
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List, Generator
import airquality.file.line.abc as lineabc


# ------------------------------- GeonamesLineType ------------------------------- #
class GeonamesLineType(lineabc.LineTypeABC):

    def __init__(self, line: List[str]):
        self._line = line

    @property
    def country_code(self) -> str:
        return self._line[0]

    @property
    def postal_code(self) -> str:
        return self._line[1]

    @property
    def place_name(self) -> str:
        return self._line[2]

    @property
    def state(self) -> str:
        return self._line[3]

    @property
    def province(self) -> str:
        return self._line[5]

    @property
    def geom(self) -> lineabc.Geolocation:
        return lineabc.Geolocation(latitude=self._line[9], longitude=self._line[10])


# ------------------------------- GeonamesLineBuilder ------------------------------- #
class GeonamesLineBuilder(lineabc.LineBuilderABC):

    ################################ build_lines() ################################
    def build(self, parsed_lines: Generator[List[str], None, None]) -> Generator[GeonamesLineType, None, None]:
        for line in parsed_lines:
            yield GeonamesLineType(line)
