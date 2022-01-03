######################################################
#
# Author: Davide Colombo
# Date: 30/12/21 15:58
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import psycopg2
from psycopg2 import connect
from abc import abstractmethod


class DatabaseError(Exception):
    """
    An *Exception* that defines is raise when a database-side error occur.
    """

    def __init__(self, cause: str):
        self.cause = cause

    def __repr__(self):
        return f"{type(self).__name__}(cause={self.cause})"


class DatabaseAdapter(object):
    """
    An *object* interface that implements the context manager interface methods and defines four methods
    for database interaction:

    - fetchone: asks the database for the first response among all the responses.
    - fetchall: asks the database all the found responses.
    - execute:  execute a query that change the database status without return anything.
    - close:    close the database connection.

    """

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        if exc_type is not None:
            if issubclass(exc_type, psycopg2.Error):
                raise DatabaseError(cause=exc_val)

    @abstractmethod
    def fetchone(self, query: str):
        pass

    @abstractmethod
    def fetchall(self, query: str):
        pass

    @abstractmethod
    def execute(self, query: str):
        pass

    @abstractmethod
    def close(self):
        pass


class Psycopg2Adapter(DatabaseAdapter):
    """
    A *DatabaseAdapter* that knows how to open a database connection using *psycopg2* module.
    """

    def __init__(self, dbname: str, user: str, password: str, host: str, port: str):
        self.conn = connect(dbname=dbname, user=user, password=password, host=host, port=port)

    def fetchone(self, query: str):
        with self.conn.cursor() as cur:
            cur.execute(query)
            self.conn.commit()
            return cur.fetchone()

    def fetchall(self, query: str):
        with self.conn.cursor() as cur:
            cur.execute(query)
            self.conn.commit()
            return cur.fetchall()

    def execute(self, query: str):
        with self.conn.cursor() as cur:
            cur.execute(query)
            self.conn.commit()

    def close(self):
        self.conn.close()

    def __repr__(self):
        return f"{type(self).__name__}(conn={self.conn!r})"
