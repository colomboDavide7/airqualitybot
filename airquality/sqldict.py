######################################################
#
# Author: Davide Colombo
# Date: 18/12/21 16:13
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from operator import itemgetter
from collections.abc import Mapping, MutableMapping
from airquality.sqltable import SQLTableABC


############################################# FrozenSQLDict(Mapping) #############################################
class FrozenSQLDict(Mapping):

    def __init__(self, table: SQLTableABC):
        self.table = table

    def __getitem__(self, key):
        #  AND {self.table.alias}.{self.table.pkey}={key}
        row = self.table.dbadapter.fetch_one(
            f"SELECT {self.table.join_cols} FROM {self.table.schema}.{self.table.name} AS {self.table.alias} "
            f"{self.table.select_key_condition(key)};"
        )
        if row is None:
            raise KeyError(f"{type(self).__name__} in __getitem__(): cannot found row indexed at '{key}' in table {self.table!r}")
        return row

    def __iter__(self):
        rows = self.table.dbadapter.fetch_all(
            f"SELECT {self.table.alias}.{self.table.pkey} FROM {self.table.schema}.{self.table.name} AS {self.table.alias} "
            f"{self.table.select_condition()};"
        )
        return map(itemgetter(0), rows)

    def __len__(self):
        row = self.table.dbadapter.fetch_one(
            f"SELECT COUNT(*) FROM {self.table.schema}.{self.table.name} AS {self.table.alias} {self.table.select_condition()};"
        )
        return row[0]

    def __repr__(self):
        return f"{type(self).__name__}(table={self.table!r})"


########################################### MutableSQLDict(MutableMapping) ###########################################
class MutableSQLDict(MutableMapping):

    def __init__(self, sqldict: FrozenSQLDict):
        self.sqldict = sqldict

    @property
    def start_id(self) -> int:
        row = self.sqldict.table.dbadapter.fetch_one(
            f"SELECT MAX({self.sqldict.table.pkey}) FROM {self.sqldict.table.schema}.{self.sqldict.table.name};"
        )
        return 1 if row[0] is None else row[0] + 1

    def __getitem__(self, key):
        return self.sqldict.__getitem__(key)

    def __iter__(self):
        return self.sqldict.__iter__()

    def __len__(self):
        return self.sqldict.__len__()

    def __setitem__(self, key, value):
        if key in self:
            del self[key]
        self.sqldict.table.dbadapter.execute(
            f"INSERT INTO {self.sqldict.table.schema}.{self.sqldict.table.name} VALUES ({key}, {value});"
        )

    def __delitem__(self, key):
        if key not in self:
            raise KeyError(f"{self.__class__.__name__} in __delitem__(): cannot found record indexed by '{key}' in {self.sqldict!r}")
        self.sqldict.table.dbadapter.execute(
            f"DELETE FROM {self.sqldict.table.schema}.{self.sqldict.table.name} AS {self.sqldict.table.alias} "
            f"{self.sqldict.table.delete_key_condition(key)};"
        )

    def __repr__(self):
        return f"{type(self).__name__}(sqldict={self.sqldict!r})"


###################################### HeavyweightMutableSQLDict(MutableMapping) ######################################
class HeavyweightMutableSQLDict(MutableMapping):

    def __init__(self, sqldict: FrozenSQLDict):
        self.sqldict = sqldict
        self._heavyweight_values = ""

    @property
    def start_id(self) -> int:
        row = self.sqldict.table.dbadapter.fetch_one(
            f"SELECT MAX({self.sqldict.table.pkey}) FROM {self.sqldict.table.schema}.{self.sqldict.table.name};"
        )
        return 1 if row[0] is None else row[0] + 1

    def commit(self):
        if not self._heavyweight_values:
            raise ValueError(f"{self.__class__.__name__} in commit(): expected not empty values in {self.sqldict!r}")
        self.sqldict.table.dbadapter.execute(
            f"INSERT INTO {self.sqldict.table.schema}.{self.sqldict.table.name} VALUES {self._heavyweight_values.strip(',')};"
        )
        self._heavyweight_values = ""

    def __getitem__(self, key):
        return self.sqldict.__getitem__(key)

    def __iter__(self):
        return self.sqldict.__iter__()

    def __len__(self):
        return self.sqldict.__len__()

    def __setitem__(self, key, value):
        self._heavyweight_values += f"({key}, {value}),"

    def __delitem__(self, key):
        """For future implementation it can be used for deleting multiple records at a time."""
        pass

    def __repr__(self):
        return f"{type(self).__name__}(sqldict={self.sqldict!r})"
