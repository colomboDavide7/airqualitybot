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
import airquality.logger.loggable as log


class DatabaseAdapter(log.Loggable):

    def __init__(self):
        super(DatabaseAdapter, self).__init__()

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

    def __init__(self, connection_string: str):
        super(Psycopg2DatabaseAdapter, self).__init__()
        self.connection_string = connection_string
        self.conn = None

    def open_conn(self):
        try:
            self.log_info(f"{Psycopg2DatabaseAdapter.__name__}: try to open database connection...")
            self.conn = psycopg2.connect(self.connection_string)
        except psycopg2.Error as err:
            raise SystemExit(f"{Psycopg2DatabaseAdapter.__name__}: bad connection string => {err!s}")
        self.log_info(f"{Psycopg2DatabaseAdapter.__name__}: done")

    def send(self, query: str):

        self.log_info(f"{Psycopg2DatabaseAdapter.__name__}: try to send query...")
        if self.conn is None:
            raise SystemExit(f"{Psycopg2DatabaseAdapter.__name__}: bad operation => connection is close")
        try:
            answer = ""
            cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()
            if query.startswith("SELECT"):
                answer = cursor.fetchall()
        except psycopg2.Error as err:
            raise SystemExit(f"{Psycopg2DatabaseAdapter.__name__}: bad query => {err!s}")

        self.log_info(f"{Psycopg2DatabaseAdapter.__name__}: done")
        return answer

    def close_conn(self):
        try:
            self.log_info(f"{Psycopg2DatabaseAdapter.__name__}: try to close database connection...")
            self.conn.close()
        except psycopg2.InterfaceError as err:
            raise SystemExit(f"{Psycopg2DatabaseAdapter.__name__}: bad operation => {err!s}")
        self.log_info(f"{Psycopg2DatabaseAdapter.__name__}: done")
