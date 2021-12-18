######################################################
#
# Author: Davide Colombo
# Date: 18/12/21 16:13
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import psycopg2
from typing import List
from operator import itemgetter
from abc import ABC, abstractmethod
from collections.abc import Mapping, MutableMapping


class SelectOnlyABC(Mapping, ABC):

    def __init__(self, dbconn: str, table: str, pkey: str, selected_cols: List[str], schema="level0_raw"):
        self.dbconn = psycopg2.connect(dbconn)
        self.table = table
        self.pkey = pkey
        self.schema = schema
        self._selected_cols = selected_cols
        self._joined_cols = ""

    def join_cols(self) -> str:
        if not self._joined_cols:
            self._joined_cols = ','.join(self._selected_cols)
        return self._joined_cols

    def close(self):
        self.dbconn.close()


class MultipleInsertABC(MutableMapping):

    @abstractmethod
    def insert(self) -> None:
        pass

    @abstractmethod
    def max_id(self):
        pass


class SelectInsertDict(SelectOnlyABC, MultipleInsertABC):

    def __init__(self, table: str, dbconn: str, pkey: str, selected_cols: List[str], schema="level0_raw"):
        super(SelectInsertDict, self).__init__(dbconn=dbconn, table=table, pkey=pkey, selected_cols=selected_cols, schema=schema)
        self.values = ""

    def insert(self):
        """Insert multiple elements """
        if not self.values:
            raise ValueError(f"{type(self).__name__} cannot insert '{self.values}' values")
        with self.dbconn.cursor() as cur:
            cur.execute(f"INSERT INTO {self.schema}.{self.table} VALUES {self.values.strip(',')};")
            self.dbconn.commit()
            self.values = ""

    def __setitem__(self, key, value) -> None:
        self.values += f"({key}, {value}),"

    def __delitem__(self, value) -> None:
        pass

    def __getitem__(self, key):
        with self.dbconn.cursor() as cur:
            cur.execute(f"SELECT {self.join_cols()} FROM {self.schema}.{self.table} WHERE {self.pkey}={key};")
            self.dbconn.commit()
            row = cur.fetchone()
            if row is None:
                raise KeyError(f"{type(self).__name__} cannot found row indexed at {self.pkey}={key}")
            return row

    def __iter__(self):
        with self.dbconn.cursor() as cur:
            cur.execute(f"SELECT {self.pkey} FROM {self.schema}.{self.table};")
            self.dbconn.commit()
            return map(itemgetter(0), cur.fetchall())

    def __len__(self):
        with self.dbconn.cursor() as cur:
            cur.execute(f"SELECT COUNT(*) FROM {self.schema}.{self.table};")
            self.dbconn.commit()
            return cur.fetchone()[0]

    def __repr__(self):
        return f"{type(self).__name__}(dbconn={self.dbconn!r}, table={self.table}, pkey={self.pkey}, " \
               f"selected_cols={self.join_cols()}, schema={self.schema})"

    def max_id(self) -> int:
        with self.dbconn.cursor() as cur:
            cur.execute(f"SELECT MAX({self.pkey}) FROM {self.schema}.{self.table};")
            self.dbconn.commit()
            x_id = cur.fetchone()[0]
            return 1 if x_id is None else x_id+1


class SelectWhereABC(Mapping, ABC):

    @abstractmethod
    def filter_condition(self) -> str:
        pass


class SelectOnlyWhereDict(SelectOnlyABC, SelectWhereABC):

    def __init__(self, dbconn: str, table: str, pkey: str, selected_cols: List[str], filter_attr: str, filter_value: str, schema="level0_raw"):
        super(SelectOnlyWhereDict, self).__init__(dbconn=dbconn, table=table, pkey=pkey, selected_cols=selected_cols, schema=schema)
        self.filter_attr = filter_attr
        self.filter_value = filter_value
        self._filter_cond = ""

    def __getitem__(self, key):
        with self.dbconn.cursor() as cur:
            cur.execute(f"SELECT {self.join_cols()} FROM {self.schema}.{self.table} WHERE {self.filter_condition()} AND {self.pkey}={key};")
            self.dbconn.commit()
            row = cur.fetchone()
            if row is None:
                raise KeyError(f"{type(self).__name__} cannot found row at {self.pkey}={key} intersected to {self.filter_condition()}")
            return row

    def __iter__(self):
        with self.dbconn.cursor() as cur:
            cur.execute(f"SELECT {self.pkey} FROM {self.schema}.{self.table} WHERE {self.filter_condition()};")
            self.dbconn.commit()
            return map(itemgetter(0), cur.fetchall())

    def __len__(self):
        with self.dbconn.cursor() as cur:
            cur.execute(f"SELECT COUNT(*) FROM {self.schema}.{self.table} WHERE {self.filter_condition()};")
            self.dbconn.cursor()
            return cur.fetchone()[0]

    def filter_condition(self) -> str:
        if not self._filter_cond:
            self._filter_cond = f"{self.filter_attr} ILIKE '%{self.filter_value}%'"
        return self._filter_cond
