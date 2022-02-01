######################################################
#
# Author: Davide Colombo
# Date: 30/12/21 15:58
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import logging

_LOGGER = logging.getLogger(__name__)

######################################################
from psycopg2 import connect
from abc import ABC, abstractmethod


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
        *psycopg2.Error*    the exceptions defined in the psycopg2 module.

    """

    def __init__(self, dbname: str, user: str, password: str, host: str, port: str):
        self.conn = connect(dbname=dbname, user=user, password=password, host=host, port=port)
        self.conn.autocommit = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        _LOGGER.debug('closing database connection')
        self.close()
        if exc_type is not None:
            _LOGGER.exception(exc_val)
            raise exc_type(exc_val) from exc_tb

    def fetchone(self, query: str):
        with self.conn.cursor() as cur:
            cur.execute(query)
            # self.conn.commit()
            return cur.fetchone()

    def fetchall(self, query: str):
        with self.conn.cursor() as cur:
            cur.execute(query)
            # self.conn.commit()
            return cur.fetchall()

    def execute(self, query: str):
        print(30*"!" + "executing query" + 30*"!")
        with self.conn.cursor() as cur:
            cur.execute(query)
            # self.conn.commit()
            print(30 * "!" + "done" + 30 * "!")

    def close(self):
        self.conn.close()

    def __repr__(self):
        return f"{type(self).__name__}(conn={self.conn!r})"
