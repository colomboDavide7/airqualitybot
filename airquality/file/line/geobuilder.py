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
import airquality.types.geonames as gntypes


class LineBuilder(log.Loggable, abc.ABC):

    def __init__(self, log_filename="log"):
        super(LineBuilder, self).__init__(log_filename=log_filename)

    @abc.abstractmethod
    def build_lines(self, parsed_lines: Generator[List[str],  None, None]):
        pass


class GeonamesLineBuilder(LineBuilder):

    def __init__(self, log_filename="log"):
        super(GeonamesLineBuilder, self).__init__(log_filename=log_filename)

    def build_lines(self, parsed_lines: Generator[List[str],  None, None]) -> Generator[gntypes.GeonamesLine,  None, None]:
        return (gntypes.GeonamesLine(
                    country_code=line[0], postal_code=line[1], place_name=line[2], state=line[3], province=line[5]
                ) for line in parsed_lines)
