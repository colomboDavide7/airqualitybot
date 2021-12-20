######################################################
#
# Author: Davide Colombo
# Date: 19/12/21 11:35
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List
from abc import ABC, abstractmethod


############################################# SQLTableABC(ABC) #############################################
class SQLTableABC(ABC):

    def __init__(self, table_name: str, pkey: str, selected_cols: List[str], schema="level0_raw", alias="t"):
        self.name = table_name
        self.alias = alias
        self.pkey = pkey
        self.schema = schema
        self.selected_cols = selected_cols
        self._join_cols = ""

    @property
    def join_cols(self) -> str:
        if not self._join_cols:
            self._join_cols = ','.join(f"{self.alias}.{col}" for col in self.selected_cols)
        return self._join_cols

    @abstractmethod
    def select_condition(self) -> str:
        pass

    @abstractmethod
    def select_key_condition(self, key) -> str:
        pass

    @abstractmethod
    def delete_key_condition(self, key) -> str:
        pass

    def __repr__(self):
        return f"{type(self).__name__}(table_name={self.name}, pkey={self.pkey}, " \
               f"selected_cols={self.join_cols}, schema={self.schema}, alias={self.alias})"


############################################# SQLTable(SQLTableABC) #############################################
class SQLTable(SQLTableABC):

    def __init__(self, table_name: str, pkey: str, selected_cols: List[str], schema="level0_raw", alias="t"):
        super(SQLTable, self).__init__(table_name=table_name, pkey=pkey, selected_cols=selected_cols, schema=schema, alias=alias)

    def select_condition(self) -> str:
        return ""

    def select_key_condition(self, key) -> str:
        return f"WHERE {self.alias}.{self.pkey}={key}"

    def delete_key_condition(self, key) -> str:
        return self.select_key_condition(key)


############################################# JoinSQLTable(SQLTableABC) #############################################
class JoinSQLTable(SQLTableABC):

    def __init__(
        self, table_name: str, pkey: str, fkey: str, selected_cols: List[str], join_table: SQLTableABC, schema="level0_raw", alias="t"
    ):
        super(JoinSQLTable, self).__init__(table_name=table_name, pkey=pkey, selected_cols=selected_cols, schema=schema, alias=alias)
        self.join_table = join_table
        self.fkey = fkey
        self._join_cond = ""

    @property
    def join_cond(self) -> str:
        if not self._join_cond:
            self._join_cond = f"INNER JOIN {self.join_table.schema}.{self.join_table.name} AS {self.join_table.alias} " \
                              f"ON {self.alias}.{self.fkey}={self.join_table.alias}.{self.join_table.pkey}"
        return self._join_cond

    def select_condition(self) -> str:
        return self.join_cond + f" {self.join_table.select_condition()}"

    def select_key_condition(self, key) -> str:
        return f"{self.select_condition()} AND {self.alias}.{self.pkey}={key}"

    def delete_key_condition(self, key) -> str:
        return f"WHERE {self.alias}.{self.pkey}={key}"

    def __repr__(self):
        return super(JoinSQLTable, self).__repr__().strip(')') + f", join_table={self.join_table!r})"


############################################# FilterSQLTable(SQLTableABC) #############################################
class FilterSQLTable(SQLTableABC):

    def __init__(
        self, table_name: str, pkey: str, selected_cols: List[str], filter_col: str, filter_val: str, schema="level0_raw", alias="t"
    ):
        super(FilterSQLTable, self).__init__(table_name=table_name, pkey=pkey, selected_cols=selected_cols, schema=schema, alias=alias)
        self._filter_col = filter_col
        self._filter_val = filter_val
        self._filter_condition = ""
        self._filter_condition_with_key = ""

    @property
    def filt_cond(self) -> str:
        if not self._filter_condition:
            self._filter_condition = f"WHERE {self.alias}.{self._filter_col} ILIKE '%{self._filter_val}%'"
        return self._filter_condition

    def select_condition(self) -> str:
        return self.filt_cond

    def select_key_condition(self, key) -> str:
        return f"{self.filt_cond} AND {self.alias}.{self.pkey}={key}"

    def delete_key_condition(self, key) -> str:
        return self.select_key_condition(key=key)

    def __repr__(self):
        return super(FilterSQLTable, self).__repr__().strip(')') + f", filter_col={self._filter_col}, filter_val={self._filter_val})"
