######################################################
#
# Author: Davide Colombo
# Date: 03/12/21 17:09
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import List, Generator
import airquality.logger.loggable as log
import airquality.types.line.line as linetype
import airquality.types.postgis as pgistype


class LineBuilderABC(log.Loggable, abc.ABC):

    def __init__(self, log_filename="log"):
        super(LineBuilderABC, self).__init__(log_filename=log_filename)

    @abc.abstractmethod
    def build_lines(self, parsed_lines: Generator[List[str],  None, None]):
        pass


class GeonamesLineBuilder(LineBuilderABC):

    def __init__(self, postgis_cls=pgistype.PostgisPoint, log_filename="log"):
        super(GeonamesLineBuilder, self).__init__(log_filename=log_filename)
        self.postgis_cls = postgis_cls

    def build_lines(self, parsed_lines: Generator[List[str],  None, None]) -> Generator[linetype.GeonamesLine, None, None]:
        for line in parsed_lines:
            yield linetype.GeonamesLine(
                country_code=line[0],
                postal_code=line[1],
                place_name=line[2],
                state=line[3],
                province=line[5],
                geom=self.postgis_cls(lat=line[9], lng=line[10])
            )


class PostalcodeLineBuilder(LineBuilderABC):

    def __init__(self, log_filename="log"):
        super(PostalcodeLineBuilder, self).__init__(log_filename=log_filename)

    def build_lines(self, parsed_lines: Generator[List[str],  None, None]) -> Generator[linetype.PostalcodeLine, None, None]:
        for line in parsed_lines:
            yield linetype.PostalcodeLine(postal_code=line[0])
