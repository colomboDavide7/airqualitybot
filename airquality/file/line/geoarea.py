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

    ################################ country_code() ################################
    def country_code(self) -> str:
        try:
            item = self._line[0]
            if not item:
                raise ValueError(f"{self.__class__.__name__} found invalid value in {self.country_code.__name__} => empty string")
            return item
        except (IndexError, ValueError) as err:
            raise SystemExit(f"{self.__class__.__name__} catches {err.__class__.__name__} in {self.country_code.__name__} => {err!r}")

    ################################ postal_code() ################################
    def postal_code(self) -> str:
        try:
            item = self._line[1]
            if not item:
                raise ValueError(f"{self.__class__.__name__} found invalid value in {self.postal_code.__name__} => empty string")
            return item
        except (IndexError, ValueError) as err:
            raise SystemExit(f"{self.__class__.__name__} catches {err.__class__.__name__} in {self.postal_code.__name__} => {err!r}")

    ################################ place_name() ################################
    def place_name(self) -> str:
        try:
            item = self._line[2].replace("'", "")
            if not item:
                raise ValueError(f"{self.__class__.__name__} found invalid value in {self.place_name.__name__} => empty string")
            return item
        except (IndexError, ValueError) as err:
            raise SystemExit(f"{self.__class__.__name__} catches {err.__class__.__name__} in {self.place_name.__name__} => {err!r}")

    ################################ geolocation() ################################
    def geolocation(self) -> pgistype.PostgisABC:
        try:
            lat = self._line[9]
            lng = self._line[10]
            if not lat or not lng:
                raise ValueError(f"{self.__class__.__name__} found invalid value in {self.geolocation.__name__} => empty string")
            return self.postgis_cls(lat=self._line[9], lng=self._line[10])
        except (IndexError, ValueError) as err:
            raise SystemExit(f"{self.__class__.__name__} catches {err.__class__.__name__} in {self.geolocation.__name__} => {err!r}")

    ################################ state() ################################
    def state(self) -> str:
        try:
            item = self._line[3].replace("'", "")
            if not item:
                raise ValueError(
                    f"{self.__class__.__name__} found invalid value in {self.state.__name__} => empty string")
            return item
        except (IndexError, ValueError) as err:
            raise SystemExit(f"{self.__class__.__name__} catches {err.__class__.__name__} in {self.state.__name__} => {err!r}")

    ################################ province() ################################
    def province(self) -> str:
        try:
            item = self._line[5].replace("'", "")
            if not item:
                raise ValueError(
                    f"{self.__class__.__name__} found invalid value in {self.province.__name__} => empty string")
            return item
        except (IndexError, ValueError) as err:
            raise SystemExit(f"{self.__class__.__name__} catches {err.__class__.__name__} in {self.province.__name__} => {err!r}")


# ------------------------------- GeoareaLineBuilder ------------------------------- #
class GeoareaLineBuilder(lineabc.LineBuilderABC):

    def __init__(self, postgis_cls=pgistype.PostgisPoint):
        self.postgis_cls = postgis_cls

    ################################ build() ################################
    def build(self, parsed_lines: Generator[List[str], None, None]) -> Generator[GeoareaLineType, None, None]:
        for line in parsed_lines:
            yield GeoareaLineType(line=line, postgis_cls=self.postgis_cls)
