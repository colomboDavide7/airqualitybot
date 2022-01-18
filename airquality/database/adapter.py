######################################################
#
# Author: Davide Colombo
# Date: 30/12/21 15:58
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import logging
from psycopg2 import connect
from abc import ABC, abstractmethod


class DatabaseError(Exception):
    """
    A subclass of Exception that is raised to signal a database side issue.
    """
    pass


class DatabaseAdapter(ABC):
    """
    AbstractBaseClass that defines the basic interface for interacting with a database.
    """

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
    A class that implements the *DatabaseAdapter* interface by using psycopg2 module.

    Keyword arguments:
        *dbname*            the database name to connect.
        *user*              the username to log in the database as.
        *password*          the username's password for database login.
        *host*              the database's connection host.
        *port*              the database's connection port.

    Raises:
        *DatabaseError*     to signal that a database side error occurs.

    """

    def __init__(self, dbname: str, user: str, password: str, host: str, port: str):
        self.conn = connect(dbname=dbname, user=user, password=password, host=host, port=port)
        self._logger = logging.getLogger(__name__)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._logger.debug('closing database connection')
        self.close()
        if exc_type is not None:
            self._logger.exception(exc_val)
            raise DatabaseError(exc_val)

    def fetchone(self, query: str):
        return self._fetch(query, exec_name='fetchone')

    def fetchall(self, query: str):
        return self._fetch(query, exec_name='fetchall')

    def execute(self, query: str):
        with self.conn.cursor() as cur:
            cur.execute(query)
            self.conn.commit()

    def _fetch(self, query: str, exec_name: str):
        with self.conn.cursor() as cur:
            cur.execute(query)
            self.conn.commit()
            return getattr(cur, exec_name)()

    def close(self):
        self.conn.close()

    def __repr__(self):
        return f"{type(self).__name__}(conn={self.conn!r})"
