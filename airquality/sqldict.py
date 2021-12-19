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

    def __delitem__(self, key) -> None:
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


############################ SelectJoinOnlyWhere(SelectOnlyABC, JoinABC, WhereABC) ############################
class SelectJoinOnlyWhereDict(SelectOnlyABC, MutableMapping, JoinABC, WhereABC):
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
        super(SelectJoinOnlyWhereDict, self).__init__(table=table, pkey=pkey, dbconn=conn, selected_cols=cols_of_interest, schema=schema)
        self.join_table = join_table
        self.join_table_alias = join_table_alias
        self.join_key = join_key
        self.join_filter_col = join_filter_col
        self.join_filter_val = join_filter_val
        self._join_cond = ""
        self._filter_cond = ""

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
        return super(SelectJoinOnlyWhereDict, self).__repr__().strip(')') + \
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


############################################# SQLTable(ABC) #############################################
class SQLTableABC(ABC):

    def __init__(self, dbconn: str, table_name: str, pkey: str, selected_cols: List[str], schema="level0_raw", alias="t"):
        self.dbconn = psycopg2.connect(dbconn)
        self.name = table_name
        self.alias = alias
        self.pkey = pkey
        self.schema = schema
        self.selected_cols = selected_cols
        self._join_cols = ""

    def __repr__(self):
        return f"{self.__class__.__name__}(dbconn={self.dbconn!r}, table_name={self.name}, pkey={self.pkey}, " \
               f"selected_cols={self.join_cols}, schema={self.schema}, alias={self.alias})"

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


class SQLTable(SQLTableABC):

    def __init__(self, dbconn: str, table_name: str, pkey: str, selected_cols: List[str], schema="level0_raw", alias="t"):
        super(SQLTable, self).__init__(
            dbconn=dbconn, table_name=table_name, pkey=pkey, selected_cols=selected_cols, schema=schema, alias=alias
        )

    def select_condition(self) -> str:
        return ""

    def select_key_condition(self, key) -> str:
        return f"WHERE {self.alias}.{self.pkey}={key}"

    def delete_key_condition(self, key) -> str:
        return self.select_key_condition(key)


############################################# JoinSQLTable(SQLTableABC) #############################################
class JoinSQLTable(SQLTableABC):

    def __init__(
            self,
            dbconn: str,
            table_name: str,
            pkey: str,
            fkey: str,
            selected_cols: List[str],
            join_table: SQLTableABC,
            schema="level0_raw",
            alias="t"
    ):
        super(JoinSQLTable, self).__init__(
            dbconn=dbconn, table_name=table_name, pkey=pkey, selected_cols=selected_cols, schema=schema, alias=alias
        )
        self.join_table = join_table
        self.fkey = fkey
        self._join_cond = ""

    @property
    def join_cond(self) -> str:
        if not self._join_cond:
            self._join_cond = f"INNER JOIN {self.join_table.schema}.{self.join_table.name} AS {self.join_table.alias} " \
                              f"ON {self.alias}.{self.fkey} = {self.join_table.alias}.{self.join_table.pkey}"
        return self._join_cond

    def select_condition(self) -> str:
        return self.join_cond + f" {self.join_table.select_condition()}"

    def select_key_condition(self, key) -> str:
        return self.join_cond + f" {self.join_table.select_key_condition(key=key)}"

    def delete_key_condition(self, key) -> str:
        return f"WHERE {self.alias}.{self.pkey}={key}"


############################################# FilterSQLTable(SQLTableABC) #############################################
class FilterSQLTable(SQLTableABC):

    def __init__(
            self,
            dbconn: str,
            table_name: str,
            pkey: str,
            selected_cols: List[str],
            filter_col: str,
            filter_val: str,
            schema="level0_raw",
            alias="t"
    ):
        super(FilterSQLTable, self).__init__(
            dbconn=dbconn, table_name=table_name, pkey=pkey, selected_cols=selected_cols, schema=schema, alias=alias
        )
        self._filter_col = filter_col
        self._filter_val = filter_val
        self._filter_condition = ""
        self._filter_condition_with_key = ""

    def __repr__(self):
        return super(SQLTableABC, self).__repr__().strip(')') + \
               f", filter_col={self._filter_col}, filter_val={self._filter_val})"

    @property
    def filt_cond(self) -> str:
        if not self._filter_condition:
            self._filter_condition = f"WHERE {self.alias}.{self._filter_col} ILIKE '%{self._filter_val}%'"
        return self._filter_condition

    def select_condition(self) -> str:
        return self.filt_cond

    def select_key_condition(self, key) -> str:
        return self.filt_cond + f" AND {self.alias}.{self.pkey}={key}"

    def delete_key_condition(self, key) -> str:
        return f"{self.filt_cond} AND {self.alias}.{self.pkey}={key}"


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

    def commit(self):
        if not self._heavyweight_values:
            raise ValueError(f"{self.__class__.__name__}: cannot commit value '{self._heavyweight_values}' to {self.sqldict!r}")
        with self.sqldict.table.dbconn.cursor() as cur:
            cur.execute(f"INSERT INTO {self.sqldict.table.schema}.{self.sqldict.table.name} VALUES {self._heavyweight_values.strip(',')};")
            self.sqldict.table.dbconn.commit()
            self._heavyweight_values = ""

    @property
    def start_id(self) -> int:
        with self.sqldict.table.dbconn.cursor() as cur:
            cur.execute(f"SELECT MAX({self.sqldict.table.pkey}) FROM {self.sqldict.table.schema}.{self.sqldict.table.name};")
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
        self._heavyweight_values += f"({key}, {value}),"

    def __delitem__(self, key):
        """For future implementation it can be used for deleting multiple records at a time."""
        pass
