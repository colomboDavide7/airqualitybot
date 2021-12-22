######################################################
#
# Author: Davide Colombo
# Date: 22/12/21 10:42
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc

ST_GEOM_FROM_TEXT = "ST_GeomFromText('{geom}', {srid})"
POSTGIS_POINT = "POINT({lon} {lat})"


class ParsedFileLineABC(abc.ABC):

    def __init__(self, line: str, separator='\t', line_limit=1):
        self.separator = separator
        self.line_limit = line_limit
        self.line = line.split(separator)
        if len(self.line) != line_limit:
            raise ValueError(f"{type(self).__name__} expected line length to be 12 instead of '{len(self.line)}'")

    def __repr__(self):
        return f"{type(self).__name__}(line={self.line}, separator={self.separator}, line_limit={self.line_limit})"


class PoscodeLine(ParsedFileLineABC):

    def __init__(self, line: str, separator='\t', line_limit=1):
        super(PoscodeLine, self).__init__(line=line, separator=separator, line_limit=line_limit)

    @property
    def poscode(self) -> str:
        return self.line[0]


class GeonamesLine(ParsedFileLineABC):

    def __init__(self, line: str, separator='\t', line_limit=12):
        super(GeonamesLine, self).__init__(line=line, separator=separator, line_limit=line_limit)

    @property
    def poscode(self) -> str:
        return self.line[1]

    @property
    def country(self) -> str:
        return self.line[0]

    @property
    def place(self) -> str:
        return self.line[2].replace("'", " ")

    @property
    def province(self) -> str:
        return self.line[5].replace("'", " ")

    @property
    def state(self) -> str:
        return self.line[3].replace("'", " ")

    @property
    def geom(self) -> str:
        point = POSTGIS_POINT.format(lat=self.line[9], lon=self.line[10])
        return ST_GEOM_FROM_TEXT.format(geom=point, srid=26918)

    @property
    def sql_record(self) -> str:
        return f"'{self.poscode}', '{self.country}', '{self.place}', '{self.province}', '{self.state}', {self.geom}"
