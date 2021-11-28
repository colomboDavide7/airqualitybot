#################################################
#
# @Author: davidecolombo
# @Date: mar, 19-10-2021, 12:37
# @Description: this script defines an Abstract Base Class to_delete that wraps the 'psycopg2' module for connecting to
#               the database and execute SQL query.
#
#################################################
import abc
import psycopg2
import airquality.logger.loggable as log
import airquality.logger.util.decorator as log_decorator


################################ DATABASE ADAPTER BASE CLASS ################################
class DatabaseAdapter(log.Loggable):

    def __init__(self, log_filename="log"):
        super(DatabaseAdapter, self).__init__(log_filename=log_filename)

    @abc.abstractmethod
    def open_conn(self):
        pass

    @abc.abstractmethod
    def close_conn(self):
        pass

    @abc.abstractmethod
    def send(self, query: str):
        pass


################################ PSYCOPG2 DATABASE ADAPTER ###############################
class Psycopg2DatabaseAdapter(DatabaseAdapter):

    def __init__(self, connection_string: str, log_filename="log"):
        super(Psycopg2DatabaseAdapter, self).__init__(log_filename=log_filename)
        self.connection_string = connection_string
        self.conn = None

    @log_decorator.log_decorator()
    def open_conn(self):
        try:
            self.conn = psycopg2.connect(self.connection_string)
        except psycopg2.Error as err:
            raise SystemExit(f"{Psycopg2DatabaseAdapter.__name__}: bad connection string => {err!s}")

    @log_decorator.log_decorator()
    def send(self, query: str):
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
        return answer

    @log_decorator.log_decorator()
    def close_conn(self):
        try:
            self.conn.close()
        except psycopg2.InterfaceError as err:
            raise SystemExit(f"{Psycopg2DatabaseAdapter.__name__}: bad operation => {err!s}")
