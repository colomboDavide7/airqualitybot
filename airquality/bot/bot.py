#################################################
#
# @Author: davidecolombo
# @Date: mar, 19-10-2021, 19:11
# @Description: This module contains the BaseBot class and its subclasses
#
#################################################
import threading
from abc import ABC
from airquality.conn.conn import DatabaseConnection
from airquality.conn.builder import SQLQueryBuilder
from airquality.parser.db_resp_parser import DatabaseResponseParser


class BaseBot(ABC):
    """BaseBot abstract base class defines the interface for a bot object.

    -dbconn: connection to database
    -apiconn: connection to API
    -thread: the thread that accomplishes the work
    """

    def __init__(self, dbconn: DatabaseConnection):
        self.__dbconn = dbconn
        self.__apiconn = None
        self.__thread = threading.Thread()

    @property
    def dbconn(self):
        return self.__dbconn

    @property
    def apiconn(self):
        return self.__apiconn


    # def open_dbconn(self):
    #     """
    #     This method is used to open the connection with the database.
    #
    #     See help on 'open_conn()' method in 'conn.py' module
    #     for more information.
    #     """
    #     self.__dbconn.open_conn()
    #
    # def close_dbconn(self):
    #     """This method is used to close the connection with the database.
    #
    #     See help on 'close_conn()' method in 'conn.py' module
    #     for more information.
    #     """
    #     self.__dbconn.close_conn()

    # def send_dbconn(self):
    #     # TODO: implement 'send()' method in DatabaseConnection class
    #     self.__dbconn.send()

    def start_bot(self):
        """Start the thread associated to this class if is not alive."""
        if not self.__thread.isAlive():
            self.__thread.start()

    def stop_bot(self):
        """Stop the thread associated to this class if is alive."""
        if self.__thread.isAlive():
            pass



class BotMobile(BaseBot):
    """
    This class extends 'BaseBot' class to handle the mobile sensor data
    fetching from the API and the loading into the database.
    """

    def __init__(self, dbconn: DatabaseConnection):
        super().__init__(dbconn)

        self.dbconn.open_conn()
        query = SQLQueryBuilder.select_all_sensor_ids_by_model("Atmotube Pro")
        response = self.dbconn.send(query)
        self.__sensor_ids = DatabaseResponseParser.parse_one_field_response(response)
        if not self.__sensor_ids:
            raise SystemExit(f"{BotMobile.__name__}: ")
        print(self.__sensor_ids)



################################ FACTORY ################################
class BotFactory:
    """
    Factory class that defines only one method for creating a BaseBot
    instance depending on 'user_type' parameter.
    """

    @staticmethod
    def create_bot_from_type(user_type: str,
                             dbconn: DatabaseConnection) -> BaseBot:
        if user_type == 'atmotube':
            return BotMobile(dbconn)
        else:
            raise TypeError(f"{BotFactory.__name__}: "
                            f"invalid type '{user_type}'.")
