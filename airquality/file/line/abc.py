######################################################
#
# Author: Davide Colombo
# Date: 09/12/21 17:08
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from collections import namedtuple
from typing import Generator, List

Geolocation = namedtuple('Geolocation', ['latitude', 'longitude'])


# ------------------------------- LineTypeABC ------------------------------- #
class LineTypeABC(abc.ABC):
    pass


# ------------------------------- LineBuilderABC ------------------------------- #
class LineBuilderABC(abc.ABC):

    @abc.abstractmethod
    def build(self, parsed_lines: Generator[List[str], None, None]) -> Generator[LineTypeABC, None, None]:
        pass
