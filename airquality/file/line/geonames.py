######################################################
#
# Author: Davide Colombo
# Date: 03/12/21 17:09
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List, Generator
import airquality.file.line.abc as lineabc
import airquality.types.postgis as pgistype


# ------------------------------- GeoareaLineType ------------------------------- #
class GeoareaLineType(lineabc.GeoareaLineTypeABC):

    def __init__(self, line: List[str], postgis_cls=pgistype.PostgisPoint):
        self._line = line
        self.postgis_cls = postgis_cls

    def country_code(self) -> str:
        return self._line[0]

    def postal_code(self) -> str:
        return self._line[1]

    def place_name(self) -> str:
        return self._line[2].replace("'", "")

    def geolocation(self) -> pgistype.PostgisGeometry:
        return self.postgis_cls(lat=self._line[9], lng=self._line[10])

    def state(self) -> str:
        return self._line[3].replace("'", "")

    def province(self) -> str:
        return self._line[5].replace("'", "")


# ------------------------------- GeoareaLineBuilder ------------------------------- #
class GeoareaLineBuilder(lineabc.LineBuilderABC):

    def __init__(self, postgis_cls=pgistype.PostgisPoint):
        self.postgis_cls = postgis_cls

    ################################ build() ################################
    def build(self, parsed_lines: Generator[List[str], None, None]) -> Generator[GeoareaLineType, None, None]:
        for line in parsed_lines:
            yield GeoareaLineType(line=line, postgis_cls=self.postgis_cls)
