#################################################
#
# @Author: davidecolombo
# @Date: mar, 19-10-2021, 19:11
# @Description: this script defines the classes that use database and sensor APIs.
#
#################################################
import builtins
from abc import ABC
from airquality.database.sql_query_builder import SQLQueryBuilder
from airquality.database.db_conn_adapter import ConnectionAdapter


class BaseBot(ABC):
    """Abstract Base Class for bot objects."""

    def __init__(self):
        self.__sql_builder = None
        self.__dbconn = None

    @property
    def sqlbuilder(self):
        return self.__sql_builder

    @sqlbuilder.setter
    def sqlbuilder(self, value: SQLQueryBuilder):
        self.__sql_builder = value

    @property
    def dbconn(self):
        return self.__dbconn

    @dbconn.setter
    def dbconn(self, value: ConnectionAdapter):
        self.__dbconn = value


class BotAtmotube(BaseBot):

    def __init__(self):
        super().__init__()



################################ FACTORY ################################
class BotFactory(builtins.object):


    @staticmethod
    def create_bot_from_personality(bot_personality: str) -> BaseBot:

        if bot_personality == "atmotube":
            return BotAtmotube()
        else:
            raise SystemExit(f"{BotFactory.__name__}: invalid bot personality {bot_personality}.")
