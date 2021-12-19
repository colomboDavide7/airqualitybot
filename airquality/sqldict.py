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
        with self.table.dbconn.cursor() as cur:
            cur.execute(f"SELECT {self.table.join_cols} FROM {self.table.schema}.{self.table.name} AS {self.table.alias} "
                        f"{self.table.select_key_condition(key=key)}")
            self.table.dbconn.commit()
            row = cur.fetchone()
            if row is None:
                raise KeyError(f"{type(self).__name__}: __getitem__() cannot found row indexed at '{key}' in table {self.table!r}")
            return row

    def __iter__(self):
        with self.table.dbconn.cursor() as cur:
            cur.execute(f"SELECT {self.table.alias}.{self.table.pkey} "
                        f"FROM {self.table.schema}.{self.table.name} AS {self.table.alias} "
                        f"{self.table.select_condition()};")
            self.table.dbconn.commit()
            return map(itemgetter(0), cur.fetchall())

    def __len__(self):
        with self.table.dbconn.cursor() as cur:
            cur.execute(f"SELECT COUNT(*) FROM {self.table.schema}.{self.table.name} AS {self.table.alias}"
                        f"{self.table.select_condition()};")
            self.table.dbconn.commit()
            return cur.fetchone()[0]

    def __repr__(self):
        return self.table.__repr__()


########################################### MutableSQLDict(MutableMapping) ###########################################
class MutableSQLDict(MutableMapping):

    def __init__(self, sqldict: FrozenSQLDict):
        self.sqldict = sqldict

    @property
    def start_id(self) -> int:
        with self.sqldict.table.dbconn.cursor() as cur:
            cur.execute(
                f"SELECT MAX({self.sqldict.table.pkey}) FROM {self.sqldict.table.schema}.{self.sqldict.table.name};")
            self.sqldict.table.dbconn.commit()
            x_id = cur.fetchone()[0]
            return 1 if x_id is None else x_id + 1

    def __getitem__(self, key):
        return self.sqldict.__getitem__(key)

    def __iter__(self):
        return self.sqldict.__iter__()

    def __len__(self):
        return self.sqldict.__len__()

    def __setitem__(self, key, value):
        if key in self:
            del self[key]
        with self.sqldict.table.dbconn.cursor() as cur:
            cur.execute(f"INSERT INTO {self.sqldict.table.schema}.{self.sqldict.table.name} VALUES ({key}, {value});")
            self.sqldict.table.dbconn.commit()

    def __delitem__(self, key):
        if key not in self:
            raise KeyError(f"{self.__class__.__name__}: __delitem__() cannot found record indexed by '{key}' in {self.sqldict!r}")
        with self.sqldict.table.dbconn.cursor() as cur:
            cur.execute(f"DELETE FROM {self.sqldict.table.schema}.{self.sqldict.table.name} AS {self.sqldict.table.alias} "
                        f"{self.sqldict.table.delete_key_condition(key)};")
            self.sqldict.table.dbconn.commit()

    def __repr__(self):
        return self.sqldict.__repr__()


###################################### HeavyweightMutableSQLDict(MutableMapping) ######################################
class HeavyweightMutableSQLDict(MutableMapping):

    def __init__(self, sqldict: FrozenSQLDict):
        self.sqldict = sqldict
        self._heavyweight_values = ""

    @property
    def start_id(self) -> int:
        with self.sqldict.table.dbconn.cursor() as cur:
            cur.execute(
                f"SELECT MAX({self.sqldict.table.pkey}) FROM {self.sqldict.table.schema}.{self.sqldict.table.name};")
            self.sqldict.table.dbconn.commit()
            x_id = cur.fetchone()[0]
            return 1 if x_id is None else x_id + 1

    def commit(self):
        if not self._heavyweight_values:
            raise ValueError(f"{self.__class__.__name__}: cannot commit value '{self._heavyweight_values}' to {self.sqldict!r}")
        with self.sqldict.table.dbconn.cursor() as cur:
            cur.execute(f"INSERT INTO {self.sqldict.table.schema}.{self.sqldict.table.name} VALUES {self._heavyweight_values.strip(',')};")
            self.sqldict.table.dbconn.commit()
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
