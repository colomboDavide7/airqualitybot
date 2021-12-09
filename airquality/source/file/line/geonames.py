######################################################
#
# Author: Davide Colombo
# Date: 03/12/21 17:09
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List, Generator
import airquality.source.file.line.abc as lineabc
import airquality.types.postgis as pgistype


# ------------------------------- GeonamesLineType ------------------------------- #
class GeonamesLineType(lineabc.LineTypeABC):

    def __init__(self, line: List[str], postgis_cls=pgistype.PostgisPoint):
        self.line = line
        self.postgis_cls = postgis_cls

    @property
    def country_code(self) -> str:
        return self.line[0]

    @property
    def postal_code(self) -> str:
        return self.line[1]

    @property
    def place_name(self) -> str:
        return self.line[2]

    @property
    def state(self) -> str:
        return self.line[3]

    @property
    def province(self) -> str:
        return self.line[5]

    @property
    def geom(self) -> pgistype.PostgisGeometry:
        return self.postgis_cls(lat=self.line[9], lng=self.line[10])

    ################################ line2sql() ################################
    def line2sql(self) -> str:
        return f"('{self.postal_code}', '{self.country_code}', '{self.place_name}', '{self.province}', '{self.state}', {self.geom.geom_from_text()})"


# ------------------------------- GeonamesLineBuilder ------------------------------- #
class GeonamesLineBuilder(lineabc.LineBuilderABC):

    def __init__(self, postgis_cls=pgistype.PostgisPoint, log_filename="log"):
        super(GeonamesLineBuilder, self).__init__(log_filename=log_filename)
        self.postgis_cls = postgis_cls

    ################################ build_lines() ################################
    def build_lines(self, parsed_lines: Generator[List[str],  None, None]) -> Generator[GeonamesLineType, None, None]:
        for line in parsed_lines:
            yield GeonamesLineType(line)
