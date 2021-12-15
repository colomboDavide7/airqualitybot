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
from typing import List
import airquality.logger.loggable as log


# ------------------------------- DBConnABC ------------------------------- #
class DBConnABC(log.LoggableABC, abc.ABC):

    @abc.abstractmethod
    def close(self):
        pass

    @abc.abstractmethod
    def execute(self, query: str):
        pass


################################ shutdown() ################################
ACTIVE_CONNECTIONS: List[DBConnABC] = []


def shutdown():
    for conn in ACTIVE_CONNECTIONS:
        conn.close()
    ACTIVE_CONNECTIONS.clear()


# ------------------------------- Psycopg2DBConn ------------------------------- #
class Psycopg2DBConn(DBConnABC):

    def __init__(self, connection_string: str):
        super(Psycopg2DBConn, self).__init__()
        try:
            self._conn = psycopg2.connect(connection_string)
            ACTIVE_CONNECTIONS.append(self)
        except psycopg2.Error as err:
            raise SystemExit(f"{self.__class__.__name__} catches {err.__class__.__name__} exception in {self.__init__.__name__} => {err!r}")

    ################################ execute() ################################
    def execute(self, query: str):
        try:
            with self._conn.cursor() as cursor:
                cursor.execute(query)
                self._conn.commit()
                if query.startswith("SELECT"):
                    return cursor.fetchall()
        except psycopg2.Error as err:
            raise SystemExit(f"{self.__class__.__name__} catches {err.__class__.__name__} exception in {self.execute.__name__} => {err!r}")

    ################################ close() ################################
    def close(self):
        self._conn.close()
        self._conn = None
