#################################################
#
# @Author: davidecolombo
# @Date: mar, 19-10-2021, 12:37
# @Description: this script defines an Abstract Base Class adapter that wraps the 'psycopg2' module for connecting to
#               the database and execute SQL query.
#
#################################################
import psycopg2
from typing import Dict, Any
from abc import ABC, abstractmethod
from airquality.constants.shared_constants import EXCEPTION_HEADER


class DatabaseAdapter(ABC):

    @abstractmethod
    def open_conn(self):
        pass

    @abstractmethod
    def close_conn(self):
        pass

    @abstractmethod
    def send(self, executable_sql_query: str):
        pass


class Psycopg2DatabaseAdapter(DatabaseAdapter):

    def __init__(self, settings: Dict[str, Any]):
        self.conn = None
        try:
            self.dbname = settings['dbname']
            self.port = settings['port']
            self.host = settings['host']
            self.username = settings['username']
            self.password = settings['password']
        except KeyError as ke:
            raise SystemExit(f"{EXCEPTION_HEADER} bad 'server.json' file structure => missing key={ke!s}.")

    def open_conn(self):
        if self.conn is not None:
            raise SystemExit(f"{EXCEPTION_HEADER} {Psycopg2DatabaseAdapter.__name__} bad 'open' operation => "
                             f"connection is already open.")
        try:
            self.conn = psycopg2.connect(database=self.dbname,
                                         port=self.port,
                                         host=self.host,
                                         user=self.username,
                                         password=self.password)
        except Exception as ex:
            raise SystemExit(f"{EXCEPTION_HEADER} {Psycopg2DatabaseAdapter.__name__} bad connection => {ex!s}.")

    def send(self, executable_sql_query: str):
        if self.conn is None:
            raise SystemExit(f"{EXCEPTION_HEADER} {Psycopg2DatabaseAdapter.__name__} bad 'send' operation => "
                             f"connection is not open.")
        try:
            answer = ""
            cursor = self.conn.cursor()
            cursor.execute(executable_sql_query)
            self.conn.commit()
            if executable_sql_query.startswith("SELECT"):
                answer = cursor.fetchall()
        except Exception as err:
            raise SystemExit(f"{EXCEPTION_HEADER} {Psycopg2DatabaseAdapter.__name__} bad query => {err!s}")
        return answer

    def close_conn(self):
        if self.conn is None:
            raise SystemExit(f"{EXCEPTION_HEADER} {Psycopg2DatabaseAdapter.__name__} bad 'close' operation => "
                             f"connection is not open.")
        self.conn.close()
        self.conn = None
