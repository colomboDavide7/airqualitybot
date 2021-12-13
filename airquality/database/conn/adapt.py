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


################################ DATABASE ADAPTER BASE CLASS ################################
class DatabaseAdapter(log.LoggableABC):

    @abc.abstractmethod
    def close_conn(self):
        pass

    @abc.abstractmethod
    def send(self, query: str):
        pass


################################ shutdown() ################################
ACTIVE_ADAPTERS: List[DatabaseAdapter] = []


def shutdown():
    for adapter in ACTIVE_ADAPTERS:
        adapter.close_conn()
    ACTIVE_ADAPTERS.clear()


################################ PSYCOPG2 DATABASE ADAPTER ###############################
class Psycopg2DatabaseAdapter(DatabaseAdapter):

    def __init__(self, connection_string: str):
        super(Psycopg2DatabaseAdapter, self).__init__()
        try:
            self._conn = psycopg2.connect(connection_string)
            ACTIVE_ADAPTERS.append(self)
        except psycopg2.Error as err:
            raise SystemExit(f"{Psycopg2DatabaseAdapter.__name__}: bad connection string => {err!r}")

    def send(self, query: str):
        try:
            answer = ""
            cursor = self._conn.cursor()
            cursor.execute(query)
            self._conn.commit()
            if query.startswith("SELECT"):
                answer = cursor.fetchall()
        except psycopg2.Error as err:
            raise SystemExit(f"{self.__class__.__name__} catches {err.__class__.__name__} in {self.send.__name__} => {err!r}")
        return answer

    def close_conn(self):
        self._conn.close()
        self._conn = None
