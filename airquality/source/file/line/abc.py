######################################################
#
# Author: Davide Colombo
# Date: 09/12/21 17:08
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import Generator, List
import airquality.logger.loggable as log


# ------------------------------- LineTypeABC ------------------------------- #
class LineTypeABC(abc.ABC):
    pass


# ------------------------------- LineBuilderABC ------------------------------- #
class LineBuilderABC(log.Loggable, abc.ABC):

    def __init__(self, log_filename="log"):
        super(LineBuilderABC, self).__init__(log_filename=log_filename)

    @abc.abstractmethod
    def build_lines(self, parsed_lines: Generator[List[str], None, None]) -> Generator[LineTypeABC, None, None]:
        pass
