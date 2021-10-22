#################################################
#
# @Author: davidecolombo
# @Date: mar, 19-10-2021, 19:11
# @Description: this script defines the classes that use database and sensor APIs.
#
#################################################
import builtins
from abc import ABC, abstractmethod
from airquality.api.url_querystring_builder import URLQuerystringBuilder
from airquality.parser.db_answer_parser import DatabaseAnswerParser
from airquality.database.sql_query_builder import SQLQueryBuilder
from airquality.database.db_conn_adapter import ConnectionAdapter
from airquality.api.api_request_adapter import APIRequestAdapter
from airquality.app.session import Session


class BaseBot(ABC):
    """Abstract Base Class for bot objects."""

    def __init__(self):
        self.__dbconn = None
        self.__sql_builder = None
        self.__api_adapter = None

    @property
    def sqlbuilder(self) -> SQLQueryBuilder:
        return self.__sql_builder

    @sqlbuilder.setter
    def sqlbuilder(self, value: SQLQueryBuilder):
        self.__sql_builder = value

    @property
    def dbconn(self) -> ConnectionAdapter:
        return self.__dbconn

    @dbconn.setter
    def dbconn(self, value: ConnectionAdapter):
        self.__dbconn = value

    @property
    def apiadapter(self) -> APIRequestAdapter:
        return self.__api_adapter

    @apiadapter.setter
    def apiadapter(self, value: APIRequestAdapter):
        self.__api_adapter = value

    @abstractmethod
    def run(self):
        pass


class BotAtmotube(BaseBot):

    def __init__(self):
        super().__init__()

    def run(self):

        if not self.apiadapter:
            raise SystemExit(f"{BotAtmotube.__name__}: missing api adapter.")

        if not self.dbconn:
            raise SystemExit(f"{BotAtmotube.__name__}: missing database connection adapter.")

        if not self.sqlbuilder:
            raise SystemExit(f"{BotAtmotube.__name__}: missing sql query builder.")

        # TRY TO OPEN DATABASE ADAPTER CONNECTION
        self.dbconn.open_conn()
        Session.get_current_session().debug_msg(f"{BotAtmotube.__name__}: try to open connection to database: OK")

        # TRY TO GET SENSOR IDs
        query = self.sqlbuilder.select_sensor_ids_from_identifier("atmotube")
        answer = self.dbconn.send(query)
        ids = DatabaseAnswerParser.parse_single_attribute_answer(answer)
        Session.get_current_session().debug_msg(f"{BotAtmotube.__name__}: try to select sensor ids from identifier 'atmotube': OK")


        for sensor_id in ids:
            # TRY TO GET SENSOR API PARAMETERS
            query = self.sqlbuilder.select_api_param_from_sensor_id(sensor_id = sensor_id)
            answer = self.dbconn.send(query)
            api_param = DatabaseAnswerParser.parse_key_val_answer(answer)
            Session.get_current_session().debug_msg(f"{BotAtmotube.__name__}: try to select api parameter from sensor ids: OK")

            # ADD 'FROM DATE' TO API PARAM
            # TODO: where to insert the date ??? FOR NOW SETTING IT MANUALLY
            from_date = '2021-07-12'
            api_param["date"] = from_date

            # BUILD URL QUERYSTRING
            querystring = URLQuerystringBuilder.AT_querystring_from_date(api_param)
            Session.get_current_session().debug_msg(f"{BotAtmotube.__name__}: try to build URL querystring: OK")

################################ FACTORY ################################
class BotFactory(builtins.object):


    @staticmethod
    def create_bot_from_personality(bot_personality: str) -> BaseBot:

        if bot_personality == "atmotube":
            return BotAtmotube()
        else:
            raise SystemExit(f"{BotFactory.__name__}: invalid bot personality {bot_personality}.")
