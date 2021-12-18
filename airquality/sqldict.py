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


############################################# SelectOnlyABC(ABC) #############################################
class SelectOnlyABC(Mapping, ABC):

    def __init__(self, dbconn: str, table: str, pkey: str, selected_cols: List[str], schema="level0_raw", alias="t"):
        self.dbconn = psycopg2.connect(dbconn)
        self.table = table
        self.alias = alias
        self.pkey = pkey
        self.schema = schema
        self._selected_cols = selected_cols
        self._joined_cols = ""

    def __repr__(self):
        return f"{type(self).__name__}(dbconn={self.dbconn!r}, table={self.table}, pkey={self.pkey}, alias={self.alias}" \
               f"selected_cols={self.join_cols()}, schema={self.schema})"

    def join_cols(self) -> str:
        if not self._joined_cols:
            self._joined_cols = ','.join(self._selected_cols)
        return self._joined_cols

    def close(self):
        self.dbconn.close()


################################# MultipleInsertABC(MutableMapping, ABC) #################################
class MultipleInsertABC(MutableMapping, ABC):

    @abstractmethod
    def insert(self) -> None:
        pass

    @abstractmethod
    def max_id(self):
        pass


################################ SelectInsertDict(SelectOnlyABC, MultipleInsertABC) ################################
class SelectInsertDict(SelectOnlyABC, MultipleInsertABC):
    """
    Read-write dict class that performs multiple SQL INSERT INTO statement on 'table' table.
    The values to insert are accumulated into the '_values' instance variable and flushed away after the insertion
    happens. To commit the changes to the database, the user must call 'insert()' method.
    """

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

    def max_id(self) -> int:
        with self.dbconn.cursor() as cur:
            cur.execute(f"SELECT MAX({self.pkey}) FROM {self.schema}.{self.table};")
            self.dbconn.commit()
            x_id = cur.fetchone()[0]
            return 1 if x_id is None else x_id + 1


############################################# WhereABC(ABC) #############################################
class WhereABC(ABC):

    @abstractmethod
    def filter_condition(self) -> str:
        pass


################################# SelectOnlyWhereDict(SelectOnlyABC, WhereABC) #################################
class SelectOnlyWhereDict(SelectOnlyABC, WhereABC):
    """
    Read-only dict class that performs SQL SELECT statements on 'table' by searching for all the records which
    'filter_attr' attribute contains 'filter_value' argument.
    """

    def __init__(self, dbconn: str, table: str, pkey: str, selected_cols: List[str], filter_attr: str,
                 filter_value: str, schema="level0_raw"):
        super(SelectOnlyWhereDict, self).__init__(dbconn=dbconn, table=table, pkey=pkey, selected_cols=selected_cols, schema=schema)
        self.filter_attr = filter_attr
        self.filter_value = filter_value
        self._filter_cond = ""

    def __getitem__(self, key):
        with self.dbconn.cursor() as cur:
            cur.execute(
                f"SELECT {self.join_cols()} FROM {self.schema}.{self.table} WHERE {self.filter_condition()} AND {self.pkey}={key};")
            self.dbconn.commit()
            row = cur.fetchone()
            if row is None:
                raise KeyError(
                    f"{type(self).__name__} cannot found row at {self.pkey}={key} intersected to {self.filter_condition()}")
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


###################################### UpdateDict(SelectOnlyABC, MutableMapping) ######################################
class UpdateDict(SelectOnlyABC, MutableMapping):
    """
    Read-write dict class that allows to perform SQL updates on the 'table' table.
    The update consists in different steps:
        - __setitem__() method calls __delitem__() method if the 'key' to insert already exist
        - __delitem__() method executes a SQL DELETE statement to remove the row associated to 'key'
        - __delitem__() return the control to __setitem__() method that performs the SQL INSERT INTO statement
    """

    def __setitem__(self, key, value):
        if key in self:
            del self[key]
        with self.dbconn.cursor() as cur:
            cur.execute(f"INSERT INTO {self.schema}.{self.table} VALUES ({key}, {value});")
            self.dbconn.commit()

    def __delitem__(self, key):
        if key not in self:
            raise KeyError(f"{type(self).__name__}: __delitem__() cannot found {self.pkey}={key}")
        with self.dbconn.cursor() as cur:
            cur.execute(f"DELETE FROM {self.schema}.{self.table} WHERE {self.pkey}={key};")
            self.dbconn.commit()

    def __getitem__(self, key):
        with self.dbconn.cursor() as cur:
            cur.execute(f"SELECT {self.join_cols()} FROM {self.schema}.{self.table} WHERE {self.pkey}={key}")
            self.dbconn.commit()
            row = cur.fetchone()
            if row is None:
                raise KeyError(
                    f"{type(self).__name__}: __getitem__() cannot found {self.pkey}={key} in table {self.table}")
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


############################################# JoinABC(ABC) #############################################
class JoinABC(ABC):

    @abstractmethod
    def join_condition(self) -> str:
        pass


############################ JoinFilterDict(SelectOnlyABC, JoinABC, WhereABC) ############################
class JoinFilterDict(SelectOnlyABC, JoinABC, WhereABC):
    """
    Read-only dict class that allows to make SQL joins between 'join_table' and 'table'.
    The join is performed on 'join_key' from 'join_table' and 'pkey' from 'table'.
    Records retrieved by the 'join' statement are filtered by selecting only the records
    which 'join_filter_col' attribute of 'join_table' contains 'join_filter_val' value.
    """

    def __init__(
            self, conn: str, join_table: str, join_key: str, table: str, pkey: str, cols_of_interest: List[str],
            join_filter_col: str, join_filter_val: str, join_table_alias="j", schema="level0_raw"
    ):
        super(JoinFilterDict, self).__init__(table=table, pkey=pkey, dbconn=conn, selected_cols=cols_of_interest, schema=schema)
        self.join_table = join_table
        self.join_table_alias = join_table_alias
        self.join_key = join_key
        self.join_filter_col = join_filter_col
        self.join_filter_val = join_filter_val
        self._join_cond = ""
        self._filter_cond = ""

    def __getitem__(self, key):
        with self.dbconn.cursor() as cur:
            cur.execute(
                f"SELECT {self.join_cols()} FROM {self.schema}.{self.table} as {self.alias} {self.join_condition()} "
                f"WHERE {self.filter_condition()} AND {self.alias}.{self.pkey}={key};")
            self.dbconn.commit()
            row = cur.fetchone()
            if row is None:
                raise KeyError(key)
            return row

    def __len__(self):
        with self.dbconn.cursor() as cur:
            cur.execute(f"SELECT COUNT(*) FROM {self.schema}.{self.table} as {self.alias} {self.join_condition()} "
                        f"WHERE {self.filter_condition()};")
            self.dbconn.commit()
            return cur.fetchone()[0]

    def __iter__(self):
        with self.dbconn.cursor() as cur:
            cur.execute(
                f"SELECT {self.alias}.{self.pkey} FROM {self.schema}.{self.table} as {self.alias} {self.join_condition()} "
                f"WHERE {self.filter_condition()};")
            self.dbconn.commit()
            return map(itemgetter(0), cur.fetchall())

    def __repr__(self):
        return super(JoinFilterDict, self).__repr__().strip(')') + \
               f", join_table={self.join_table}, join_key={self.join_key}, join_table_alias={self.join_table_alias}, " \
               f"join_filter_col={self.join_filter_col}, join_filter_val={self.join_filter_val})"

    def join_condition(self) -> str:
        if not self._join_cond:
            self._join_cond = f"INNER JOIN {self.schema}.{self.join_table} as {self.join_table_alias} " \
                              f"ON {self.join_table_alias}.{self.join_key}={self.alias}.{self.pkey}"
        return self._join_cond

    def filter_condition(self) -> str:
        if not self._filter_cond:
            self._filter_cond = f"{self.join_table_alias}.{self.join_filter_col} ILIKE '%{self.join_filter_val}%'"
        return self._filter_cond
