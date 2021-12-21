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
from airquality.dbadapter import DBAdapterABC


############################################# FrozenSQLDict(Mapping) #############################################
class FrozenSQLDict(Mapping):

    def __init__(self, table: SQLTableABC, dbadapter: DBAdapterABC):
        self.table = table
        self.dbadapter = dbadapter

    def __getitem__(self, key):
        row = self.dbadapter.fetch_one(
            f"SELECT {self.table.join_cols} FROM {self.table.schema}.{self.table.name} AS {self.table.alias} "
            f"{self.table.select_key_condition(key)};"
        )
        if row is None:
            raise KeyError(f"{type(self).__name__} in __getitem__(): cannot found row indexed at '{key}' in table {self.table!r}")
        return row

    def __iter__(self):
        rows = self.dbadapter.fetch_all(
            f"SELECT {self.table.alias}.{self.table.pkey} FROM {self.table.schema}.{self.table.name} AS {self.table.alias} "
            f"{self.table.select_condition()};"
        )
        return map(itemgetter(0), rows)

    def __len__(self):
        row = self.dbadapter.fetch_one(
            f"SELECT COUNT(*) FROM {self.table.schema}.{self.table.name} AS {self.table.alias} {self.table.select_condition()};"
        )
        return row[0]

    def __repr__(self):
        return f"{type(self).__name__}(table={self.table!r}, dbadapter={self.dbadapter!r})"


########################################### MutableSQLDict(MutableMapping) ###########################################
class MutableSQLDict(FrozenSQLDict, MutableMapping):

    def __init__(self, table: SQLTableABC, dbadapter: DBAdapterABC):
        super(MutableSQLDict, self).__init__(table=table, dbadapter=dbadapter)

    @property
    def start_id(self) -> int:
        row = self.dbadapter.fetch_one(f"SELECT MAX({self.table.pkey}) FROM {self.table.schema}.{self.table.name};")
        return 1 if row[0] is None else row[0] + 1

    def __setitem__(self, key, value):
        if key in super(MutableSQLDict, self).__iter__():
            del self[key]
        self.dbadapter.execute(f"INSERT INTO {self.table.schema}.{self.table.name} VALUES ({key}, {value});")

    def __delitem__(self, key):
        if key not in super(MutableSQLDict, self).__iter__():
            raise KeyError(f"{self.__class__.__name__} in __delitem__(): cannot found record indexed by '{key}' in {self.table!r}")
        self.dbadapter.execute(
            f"DELETE FROM {self.table.schema}.{self.table.name} AS {self.table.alias} {self.table.delete_key_condition(key)};"
        )


###################################### HeavyweightMutableSQLDict(MutableMapping) ######################################
class HeavyweightMutableSQLDict(FrozenSQLDict, MutableMapping):

    def __init__(self, table: SQLTableABC, dbadapter: DBAdapterABC):
        super(HeavyweightMutableSQLDict, self).__init__(table=table, dbadapter=dbadapter)
        self._values2insert = ""

    @property
    def start_id(self) -> int:
        row = self.dbadapter.fetch_one(f"SELECT MAX({self.table.pkey}) FROM {self.table.schema}.{self.table.name};")
        return 1 if row[0] is None else row[0] + 1

    def commit(self):
        if not self._values2insert:
            raise ValueError(f"{type(self).__name__} in commit(): cannot commit empty values to {self.table!r}")
        self.dbadapter.execute(f"INSERT INTO {self.table.schema}.{self.table.name} VALUES {self._values2insert.strip(',')};")
        self._values2insert = ""

    def __setitem__(self, key, value):
        self._values2insert += f"({key}, {value}),"

    def __delitem__(self, key):
        """For future implementation it can be used for deleting multiple records at a time."""
        pass
