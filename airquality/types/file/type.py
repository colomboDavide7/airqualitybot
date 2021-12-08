######################################################
#
# Author: Davide Colombo
# Date: 08/12/21 14:36
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import Generator, List
import airquality.types.line.line as linetype


class FileTypeABC(abc.ABC):

    def __init__(self, filename: str, lines: Generator[linetype.LineABC, None, None]):
        self.filename = filename
        self.lines = lines

    @abc.abstractmethod
    def unique_lines(self) -> Generator[linetype.LineABC, None, None]:
        pass


class GeonamesFileType(FileTypeABC):

    def __init__(self, filename: str, geolines: Generator[linetype.GeonamesLine, None, None]):
        super(GeonamesFileType, self).__init__(filename=filename, lines=geolines)
        self.lines = geolines

    @property
    def country_code(self) -> str:
        return self.filename

    def unique_lines(self) -> Generator[linetype.GeonamesLine, None, None]:
        place_with_more_than_one_occurrence = set()
        for line in self.lines:
            if line.place_name not in place_with_more_than_one_occurrence:
                yield line
                place_with_more_than_one_occurrence.add(line.place_name)


class PostalcodeFileType(FileTypeABC):

    def __init__(self, filename: str, poscode_lines: Generator[linetype.PostalcodeLine, None, None]):
        super(PostalcodeFileType, self).__init__(filename=filename, lines=poscode_lines)
        self.lines = poscode_lines

    def unique_lines(self) -> Generator[linetype.PostalcodeLine, None, None]:
        poscode_with_more_than_one_occurrence = set()
        for line in self.lines:
            if line.postal_code not in poscode_with_more_than_one_occurrence:
                yield line
                poscode_with_more_than_one_occurrence.add(line.postal_code)

    @property
    def country_code(self) -> str:
        return self.filename

    @property
    def postal_codes(self) -> List[str]:
        return [line.postal_code for line in self.unique_lines()]
