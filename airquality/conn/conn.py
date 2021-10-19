#################################################
#
# @Author: davidecolombo
# @Date: mar, 19-10-2021, 12:37
# @Description: Script that defines the Connection class and its subclasses
#               and defines the ConnectionFactory and its subclasses
#
#################################################
from typing import Dict, Any
from abc import ABC, abstractmethod
import psycopg2


class Connection(ABC):

    @abstractmethod
    def open_conn(self) -> bool:
        """Abstract method for opening the connection."""
        pass

    @abstractmethod
    def close_conn(self) -> bool:
        """Abstract method for closing the connection."""
        pass

    @abstractmethod
    def send(self) -> bool:
        """Abstract method for sending things through this connection."""
        pass

    @abstractmethod
    def is_open(self) -> bool:
        """Abstract method that defines the condition for a connection to be
        closed or opened."""
        pass


class DatabaseConnection(Connection):
    """DatabaseConnection class is a wrapper class for psycopg2 connection
    object.

    - port: port number
    - dbname: database name
    -hostname: host name
    -username: a valid username for database connection
    -password: if any, the valid password for the username
    -set_ok: binary number with 5 digits that is used for checking settings
    """
    def __init__(self,
                 settings: Dict[str, Any]):
        self.__port = None
        self.__dbname = None
        self.__hostname = None
        self.__username = None
        self.__password = None
        self.__psycopg2_conn = None
        self.__set_ok = 0b00000

        if settings:
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
                    print(f"{DatabaseConnection.__name__}: "
                          f"invalid key setting '{key}' is ignored.")

        if self.__set_ok != 0b11111:
            raise SystemExit(f"{DatabaseConnection.__name__}: "
                             f"cannot instantiate a DatabaseConnection "
                             f"object without all settings arguments.")


    def close_conn(self) -> bool:
        """This method closes the connection with the postgreSQL database
        if the connection object is not None (open connection),
        otherwise a SystemExit exception is raised.

        If the connection is successfully closed, the reference to the
        'psycopg2_conn' instance variable is reset to None.

        In this way, the 'is_open()' method continues to work properly.
        """
        if not self.is_open():
            raise SystemExit(
                    f"{DatabaseConnection.__name__}: "
                    f"cannot close connection that is not opened.")
        self.__psycopg2_conn.close()
        self.__psycopg2_conn = None
        return True


    def send(self) -> bool:
        # TODO: think of creating a variable for letting the user set the
        #  query string before calling this method
        pass

    def open_conn(self) -> bool:
        """
        This method create a new psycopg2 connection object if variable
        'psycopg2_conn' is None, otherwise a SystemExit exception is raised.
        """
        if self.is_open():
            raise SystemExit(
                    f"{DatabaseConnection.__name__}: "
                    f"cannot open connection that is already opened.")
        try:
            self.__psycopg2_conn = psycopg2.connect(database = self.__dbname,
                                                    port = self.__port,
                                                    host = self.__hostname,
                                                    user = self.__username,
                                                    password = self.__password)
        except Exception as err:
            raise SystemExit(f"{DatabaseConnection.__name__}: "
                             f"{str(err)}")
        return True

    def is_open(self) -> bool:
        """Method that returns True if the psycopg2 connection object is
        not None, otherwise False."""
        return self.__psycopg2_conn is not None


################################ FACTORIES ################################
class ConnectionFactory(ABC):

    @abstractmethod
    def create_connection(self, settings: Dict[str, Any]) -> Connection:
        """
        Abstract method for creating the right Connection subclass instance.
        """
        pass


class DatabaseConnectionFactory(ConnectionFactory):

    def create_connection(self, settings: Dict[str, Any]) -> Connection:
        return DatabaseConnection(settings)
