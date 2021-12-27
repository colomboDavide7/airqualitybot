######################################################
#
# Author: Davide Colombo
# Date: 27/12/21 15:39
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List
from airquality.sqlcolumn import SQLColumnABC


class SQLColumnLink(SQLColumnABC):

    def __init__(self, columns: List[SQLColumnABC]):
        if len(columns) < 1:
            raise ValueError(f"{type(self).__name__} expected at least one column to select")
        self.columns = columns

    def selected_columns(self) -> str:
        return ','.join(f"{col.selected_columns()}" for col in self.columns)

    def __repr__(self):
        return f"{type(self).__name__}(columns={self.columns!r})"


class DecoratedSQLColumnLink(SQLColumnLink):

    def __init__(self, columns: List[SQLColumnABC], linked: SQLColumnLink):
        super(DecoratedSQLColumnLink, self).__init__(columns=columns)
        self.linked = linked

    def selected_columns(self) -> str:
        linked = self.linked.selected_columns()
        if len(self.columns) == 1:
            return linked + f",{self.columns[0].selected_columns()}"
        return linked + super(DecoratedSQLColumnLink, self).selected_columns()

    def __repr__(self):
        return super(DecoratedSQLColumnLink, self).__repr__().strip(')') + f", linked={self.linked!r}"
