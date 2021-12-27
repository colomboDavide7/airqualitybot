######################################################
#
# Author: Davide Colombo
# Date: 27/12/21 11:19
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List
from airquality.sqlsearch import SQLSearchABC


class SQLSearchLink(SQLSearchABC):

    def __init__(self, search_conditions: List[SQLSearchABC], link_keyword: str, min_len=2):
        if len(search_conditions) < min_len:
            raise ValueError(f"{type(self).__name__} expected at least {min_len} conditions to link")
        self.search_conditions = search_conditions
        self.link_keyword = link_keyword

    def search_condition(self) -> str:
        return f' {self.link_keyword} '.join(f"{s.search_condition()}" for s in self.search_conditions)

    def __repr__(self):
        return f"{type(self).__name__}(link_keyword={self.link_keyword}, search_conditions={self.search_conditions!r})"


class DecoratedSQLSearchLink(SQLSearchLink):

    def __init__(self, search_conditions: List[SQLSearchABC], link_keyword: str, linked: SQLSearchLink, min_len=1):
        super(DecoratedSQLSearchLink, self).__init__(search_conditions=search_conditions, link_keyword=link_keyword, min_len=min_len)
        self.linked = linked

    def search_condition(self) -> str:
        linked = self.linked.search_condition()
        if len(self.search_conditions) == 1:
            return linked + f' {self.link_keyword} {self.search_conditions[0].search_condition()}'
        return linked + super().search_condition()

    def __repr__(self):
        return super(DecoratedSQLSearchLink, self).__repr__().strip(')') + f", linked={self.linked!r}"
