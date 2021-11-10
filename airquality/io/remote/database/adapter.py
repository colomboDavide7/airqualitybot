#################################################
#
# @Author: davidecolombo
# @Date: mar, 19-10-2021, 12:37
# @Description: this script defines an Abstract Base Class adapter that wraps the 'psycopg2' module for connecting to
#               the database and execute SQL query.
#
#################################################
import abc
import psycopg2
from typing import Dict, Any


class DatabaseAdapter(abc.ABC):

    @abc.abstractmethod
    def open_conn(self):
        pass

    @abc.abstractmethod
    def close_conn(self):
        pass

    @abc.abstractmethod
    def send(self, query: str):
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
            raise SystemExit(f"{Psycopg2DatabaseAdapter.__name__} bad 'server.json' file structure => missing key={ke!s}.")

    def open_conn(self):
        if self.conn is not None:
            raise SystemExit(f"{Psycopg2DatabaseAdapter.__name__} bad 'open' operation => connection is already open.")
        try:
            self.conn = psycopg2.connect(database=self.dbname,
                                         port=self.port,
                                         host=self.host,
                                         user=self.username,
                                         password=self.password)
        except Exception as ex:
            raise SystemExit(f"{Psycopg2DatabaseAdapter.__name__} bad connection => {ex!s}.")

    def send(self, query: str):
        if self.conn is None:
            raise SystemExit(f"{Psycopg2DatabaseAdapter.__name__} bad 'send' operation => connection is not open.")
        try:
            answer = ""
            cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()
            if query.startswith("SELECT"):
                answer = cursor.fetchall()
        except Exception as err:
            raise SystemExit(f"{Psycopg2DatabaseAdapter.__name__} bad query => {err!s}")
        return answer

    def close_conn(self):
        if self.conn is None:
            raise SystemExit(f"{Psycopg2DatabaseAdapter.__name__} bad 'close' operation => connection is not open.")
        self.conn.close()
        self.conn = None
