######################################################
#
# Author: Davide Colombo
# Date: 03/12/21 16:38
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import List, Generator
import airquality.logger.loggable as log
import airquality.logger.util.decorator as log_decorator


def get_line_parser(separator: str, log_filename="log"):

    if separator == "\t":
        return TSVLineParser(separator=separator, log_filename=log_filename)
    else:
        raise SystemExit(f"{get_line_parser.__name__}(): bad line token separator '{separator}' => "
                         f"supported token separator are: [ \\t ]")


class LineParser(log.Loggable, abc.ABC):

    def __init__(self, separator: str, log_filename="log"):
        super(LineParser, self).__init__(log_filename=log_filename)
        self.separator = separator

    @abc.abstractmethod
    def parse_lines(self, lines: List[str]) -> Generator[List[str], None, None]:
        pass


class TSVLineParser(LineParser):

    def __init__(self, separator: str, log_filename="log"):
        super(TSVLineParser, self).__init__(separator=separator, log_filename=log_filename)

    @log_decorator.log_decorator()
    def parse_lines(self, lines: List[str]) -> Generator[List[str],  None, None]:
        return (line.strip('\n').split(self.separator) for line in lines)
