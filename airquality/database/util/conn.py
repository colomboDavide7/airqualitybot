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


class DatabaseAdapter(abc.ABC):

    @abc.abstractmethod
    def close_conn(self):
        pass

    @abc.abstractmethod
    def send(self, query: str):
        pass


class Psycopg2DatabaseAdapter(DatabaseAdapter):

    def __init__(self, connection_string: str):
        try:
            self.conn = psycopg2.connect(connection_string)
        except psycopg2.Error as err:
            raise SystemExit(f"{Psycopg2DatabaseAdapter.__name__}: bad connection string => {err!s}")

    def send(self, query: str):
        try:
            answer = ""
            cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()
            if query.startswith("SELECT"):
                answer = cursor.fetchall()
        except psycopg2.Error as err:
            raise SystemExit(f"{Psycopg2DatabaseAdapter.__name__}: bad query => {err!s}")
        return answer

    def close_conn(self):
        try:
            self.conn.close()
        except psycopg2.InterfaceError as err:
            raise SystemExit(f"{Psycopg2DatabaseAdapter.__name__}: bad operation => {err!s}")
