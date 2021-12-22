######################################################
#
# Author: Davide Colombo
# Date: 22/12/21 10:42
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
ST_GEOM_FROM_TEXT = "ST_GeomFromText('{geom}', {srid})"
POSTGIS_POINT = "POINT({lon} {lat})"


def clean_value(string: str) -> str:
    """Replace single quotes into *string* argument with a space

    >>>clean_value("O'Reilly")
    O Reilly
    """

    return string.replace("'", " ")


class GeonamesLine(object):

    def __init__(self, line: str, separator='\t'):
        self.separator = separator
        self.line = line.split(separator)
        if len(self.line) != 12:
            raise ValueError(f"{type(self).__name__} expected line length to be 12 instead of '{len(self.line)}'")

    @property
    def poscode(self) -> str:
        return self.line[1]

    @property
    def country(self) -> str:
        return self.line[0]

    @property
    def place(self) -> str:
        return clean_value(self.line[2])

    @property
    def province(self) -> str:
        return clean_value(self.line[5])

    @property
    def state(self) -> str:
        return clean_value(self.line[3])

    @property
    def geom(self) -> str:
        point = POSTGIS_POINT.format(lat=self.line[9], lon=self.line[10])
        return ST_GEOM_FROM_TEXT.format(geom=point, srid=26918)

    @property
    def sql_record(self) -> str:
        return f"'{self.poscode}', '{self.country}', '{self.place}', '{self.province}', '{self.state}', {self.geom}"

    def __repr__(self):
        return f"{type(self).__name__}(country={self.country}, poscode={self.poscode}, place={self.place}, " \
               f"province={self.province}, state={self.state}, geom={self.geom})"
