######################################################
#
# Author: Davide Colombo
# Date: 19/12/21 17:50
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import psycopg2
import psycopg2.errors as pg2err


class DatabaseAdapterError(Exception):

    def __repr__(self):
        return f"{type(self).__name__}"


class DBAdapter(object):

    def __init__(self, dbname: str, user: str, password: str, host="localhost", port="5432"):
        self._dbname = dbname
        self._user = user
        self._password = password
        self._host = host
        self._port = port
        self._conn = psycopg2.connect(database=self._dbname, user=self._user, password=self._password, host=self._host, port=self._port)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type == DatabaseAdapterError:
            print(f"{self.__class__.__name__} in __exit__(): {exc_tb}")
        self._conn.close()

    def execute(self, query: str):
        if not query.startswith("DELETE") and not query.startswith("INSERT INTO"):
            raise ValueError(f"{type(self).__name__} in execute(): expected query to begin with 'DELETE' or 'INSERT INTO'")
        try:
            with self._conn.cursor() as cur:
                cur.execute(query)
                self._conn.commit()
        except pg2err.Error as err:
            raise DatabaseAdapterError(f"{type(self).__name__} in execute(): {err!r}")

    def fetch_all(self, query: str):
        if not query.startswith("SELECT"):
            raise ValueError(f"{type(self).__name__} in fetch_all(): expected query to begin with 'SELECT'")
        try:
            with self._conn.cursor() as cur:
                cur.execute(query)
                self._conn.commit()
                return cur.fetchall()
        except pg2err.Error as err:
            raise DatabaseAdapterError(f"{type(self).__name__} in fetch_all(): {err!r}")

    def fetch_one(self, query):
        if not query.startswith("SELECT"):
            raise ValueError(f"{type(self).__name__} in fetch_one(): expected query to begin with 'SELECT'")
        try:
            with self._conn.cursor() as cur:
                cur.execute(query)
                self._conn.commit()
                return cur.fetchone()
        except pg2err.Error as err:
            raise DatabaseAdapterError(f"{type(self).__name__} in fetch_one(): {err!r}")

    def __repr__(self):
        return f"{type(self).__name__}(dbname={self._dbname}, user={self._user}, password=XXX, host={self._host}, port={self._port})"
