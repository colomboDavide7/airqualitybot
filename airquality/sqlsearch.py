######################################################
#
# Author: Davide Colombo
# Date: 27/12/21 10:07
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from abc import ABC, abstractmethod


class SQLSearchABC(ABC):

    @abstractmethod
    def search_condition(self) -> str:
        pass


class SQLSearch(SQLSearchABC):

    def __init__(self, search_column: str, search_value: str, alias="t"):
        self._search_column = search_column
        self._search_value = search_value
        self.alias = alias

    @abstractmethod
    def keyword(self) -> str:
        pass

    @abstractmethod
    def search_value(self) -> str:
        pass

    def search_condition(self) -> str:
        return f"{self.alias}.{self._search_column} {self.keyword()} {self.search_value()}"

    def __repr__(self):
        return f"{type(self).__name__}(search_column='{self._search_column}', keyword='{self.keyword()}', " \
               f"search_value={self.search_value()})"


class EqualSearch(SQLSearch):

    def keyword(self):
        return "="

    def search_value(self) -> str:
        return f"'{self._search_value}'"


class ILIKESearch(SQLSearch):

    def keyword(self):
        return "ILIKE"

    def search_value(self) -> str:
        return f"'%{self._search_value}%'"


class INSearch(SQLSearch):

    def keyword(self):
        return "IN"

    def search_value(self) -> str:
        values = self._search_value.split(',')
        joined = ','.join(f"'{v}'" for v in values)
        return f"({joined})"
