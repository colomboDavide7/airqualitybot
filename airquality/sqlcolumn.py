######################################################
#
# Author: Davide Colombo
# Date: 27/12/21 15:22
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from abc import ABC, abstractmethod


class SQLColumnABC(ABC):

    @abstractmethod
    def selected_columns(self) -> str:
        pass


class SQLColumn(SQLColumnABC):
    COL_KW = "col"

    def __init__(self, target_column: str, alias="t"):
        self.target_column = target_column
        self.alias = alias

    def column_template(self) -> str:
        return "{%s}" % self.COL_KW

    def selected_columns(self) -> str:
        return self.column_template().format(col=f"{self.alias}.{self.target_column}")

    def __repr__(self):
        return f"{type(self).__name__}(target_column={self.target_column}, alias={self.alias})"


class CountColumn(SQLColumn):

    def column_template(self) -> str:
        return "COUNT({%s})" % self.COL_KW


class MaxColumn(SQLColumn):

    def column_template(self) -> str:
        return "MAX({%s})" % self.COL_KW


class ST_X_Column(SQLColumn):

    def column_template(self) -> str:
        return "ST_X({%s})" % self.COL_KW


class ST_Y_Column(SQLColumn):

    def column_template(self) -> str:
        return "ST_Y({%s})" % self.COL_KW
