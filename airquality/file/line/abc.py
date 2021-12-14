######################################################
#
# Author: Davide Colombo
# Date: 09/12/21 17:08
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import Generator, List
import airquality.types.postgis as pgistype


# ------------------------------- LineTypeABC ------------------------------- #
class LineTypeABC(abc.ABC):
    pass


# ------------------------------- GeoareaLineTypeABC ------------------------------- #
class GeoareaLineTypeABC(LineTypeABC, abc.ABC):

    @abc.abstractmethod
    def geolocation(self) -> pgistype.PostgisABC:
        pass

    @abc.abstractmethod
    def postal_code(self) -> str:
        pass

    @abc.abstractmethod
    def place_name(self) -> str:
        pass

    @abc.abstractmethod
    def country_code(self) -> str:
        pass

    @abc.abstractmethod
    def state(self) -> str:
        pass

    @abc.abstractmethod
    def province(self) -> str:
        pass


# ------------------------------- LineBuilderABC ------------------------------- #
class LineBuilderABC(abc.ABC):

    @abc.abstractmethod
    def build(self, parsed_lines: Generator[List[str], None, None]) -> Generator[LineTypeABC, None, None]:
        pass
