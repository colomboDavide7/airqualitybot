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
from airquality.constants.shared_constants import EMPTY_STRING, EMPTY_DICT


class ConnectionAdapter(ABC):

    @abstractmethod
    def open_conn(self) -> bool:
        """Abstract method for opening the connection."""
        pass

    @abstractmethod
    def close_conn(self) -> bool:
        """Abstract method for closing the connection."""
        pass

    @abstractmethod
    def send(self, msg_str: str):
        """Abstract method for executing SQL statement through this connection."""
        pass

    @abstractmethod
    def is_open(self) -> bool:
        """Abstract method that defines the condition for a connection to be closed or opened."""
        pass


class Psycopg2ConnectionAdapter(ConnectionAdapter):
    """This class is a wrapper for psycopg2 database connection object.

    -port:      port number
    -dbname:    database name
    -hostname:  host name
    -username:  a valid username for database connection
    -password:  if any, the valid password for the username
    -set_ok:    binary number with 5 digits that is used for checking settings"""

    def __init__(self, settings: Dict[str, Any]):
        self.__port = None
        self.__dbname = None
        self.__hostname = None
        self.__username = None
        self.__password = None
        self.__psycopg2_conn = None
        self.__set_ok = 0b00000

        if settings != EMPTY_DICT:
            for key, val in settings.items():
                if key == 'port':
                    self.__port = val
                    self.__set_ok |= 0b00001
                elif key == 'host':
                    self.__hostname = val
                    self.__set_ok |= 0b00010
                elif key == 'dbname':
                    self.__dbname = val
                    self.__set_ok |= 0b00100
                elif key == 'username':
                    self.__username = val
                    self.__set_ok |= 0b01000
                elif key == 'password':
                    self.__password = val
                    self.__set_ok |= 0b10000
                else:
                    print(f"{Psycopg2ConnectionAdapter.__name__}: invalid key setting '{key}' is ignored.")

        if self.__set_ok != 0b11111:
            raise SystemExit(
                f"{Psycopg2ConnectionAdapter.__name__}: cannot instantiate a DatabaseConnection object without "
                f"all settings arguments in method '{Psycopg2ConnectionAdapter.__init__.__name__}()'.")

    def open_conn(self) -> bool:
        """This method create a new psycopg2 connection object.

        If connection is already opened, SystemExit exception is raised."""

        if self.is_open():
            raise SystemExit(f"{Psycopg2ConnectionAdapter.__name__}: cannot open connection that is already opened.")

        try:
            self.__psycopg2_conn = psycopg2.connect(
                database=self.__dbname,
                port=self.__port,
                host=self.__hostname,
                user=self.__username,
                password=self.__password
            )
        except Exception as err:
            raise SystemExit(f"{Psycopg2ConnectionAdapter.__name__}: {str(err)}")
        return True

    def send(self, executable_sql_query: str):
        """This method takes an executable SQL statement string as argument and asks the psycopg2 cursor to execute it.

        If connection is close, SystemExit exception is raised.
        If the argument string is not a valid SQL statement, SystemExit exception is raised."""

        if not self.is_open():
            raise SystemExit(f"{Psycopg2ConnectionAdapter.__name__}: cannot send message when connection is closed.")

        answer = ""
        if executable_sql_query == EMPTY_STRING:
            return answer

        try:
            cursor = self.__psycopg2_conn.cursor()
            cursor.execute(executable_sql_query)
            self.__psycopg2_conn.commit()
            if executable_sql_query.startswith("SELECT"):
                answer = cursor.fetchall()
        except Exception as err:
            self.close_conn()
            raise SystemExit(f"{Psycopg2ConnectionAdapter.__name__}: {str(err)}")
        return answer

    def close_conn(self) -> bool:
        """This method closes the psycopg2 database connection.

        If connection is not open, SystemExit exception is raised."""

        if not self.is_open():
            raise SystemExit(f"{Psycopg2ConnectionAdapter.__name__}: cannot close connection that is not open.")

        self.__psycopg2_conn.close()
        self.__psycopg2_conn = None
        return True

    def is_open(self) -> bool:
        """Method that returns True if the psycopg2 connection object is not None, otherwise False."""

        return self.__psycopg2_conn is not None


################################ FACTORIES ################################
class ConnectionAdapterFactory(ABC):

    @abstractmethod
    def create_database_connection_adapter(self, settings: Dict[str, Any]) -> ConnectionAdapter:
        """Abstract method for creating the right Connection subclass instance."""
        pass


class Psycopg2ConnectionAdapterFactory(ConnectionAdapterFactory):

    def create_database_connection_adapter(self, settings: Dict[str, Any]) -> Psycopg2ConnectionAdapter:
        return Psycopg2ConnectionAdapter(settings)
