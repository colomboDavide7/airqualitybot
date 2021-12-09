######################################################
#
# Author: Davide Colombo
# Date: 09/12/21 17:23
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import Tuple, Generator
import airquality.source.abc as srcabc
import airquality.source.file.line.abc as lineabc


def get_filename(file: str) -> str:
    return file.split('.')[0]


# ------------------------------- FileTypeABC ------------------------------- #
class FileTypeABC(abc.ABC):

    def __init__(self, filename: str, lines: Generator[lineabc.LineTypeABC, None, None]):
        self.filename = filename
        self.lines = lines

    @abc.abstractmethod
    def unique_lines(self) -> Generator[lineabc.LineTypeABC, None, None]:
        pass


# ------------------------------- FileSourceABC ------------------------------- #
class FileSourceABC(srcabc.SourceABC, abc.ABC):

    @abc.abstractmethod
    def get(self) -> Tuple[FileTypeABC]:
        pass

    @abc.abstractmethod
    def retrieve(self, filename: str) -> FileTypeABC:
        pass
