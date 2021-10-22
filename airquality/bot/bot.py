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
from airquality.picker.api_packet_picker import APIPacketPicket
from airquality.parser.file_parser import FileParserFactory
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

    SENSOR_IDENTIFIER = "atmotube"

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
        query = self.sqlbuilder.select_sensor_ids_from_identifier(identifier = BotAtmotube.SENSOR_IDENTIFIER)
        answer = self.dbconn.send(query)
        ids = DatabaseAnswerParser.parse_single_attribute_answer(answer)
        Session.get_current_session().debug_msg(f"{BotAtmotube.__name__}: try to select sensor ids from identifier: OK")

        # TRY TO GET MEASURE PARAM (ID, CODE) FROM IDENTIFIER
        query = self.sqlbuilder.select_measure_param_from_identifier(identifier = BotAtmotube.SENSOR_IDENTIFIER)
        answer = self.dbconn.send(query)
        id_code_dict = DatabaseAnswerParser.parse_key_val_answer(answer)
        Session.get_current_session().debug_msg(f"{BotAtmotube.__name__}: try to select measure param id from identifier: OK")

        for sensor_id in ids:
            Session.get_current_session().debug_msg(f"---------- SENSOR {sensor_id} ----------")
            # TRY TO GET SENSOR API PARAMETERS
            query = self.sqlbuilder.select_api_param_from_sensor_id(sensor_id = sensor_id)
            answer = self.dbconn.send(query)
            api_param = DatabaseAnswerParser.parse_key_val_answer(answer)
            Session.get_current_session().debug_msg(f"{BotAtmotube.__name__}: try to select api parameter from sensor ids: OK")


            # TODO: run sensors request on a different thread x sensor


            # ADD 'FROM DATE' TO API PARAM
            # TODO: where to insert the date ??? FOR NOW SETTING IT MANUALLY
            from_date = '2021-07-12'
            api_param["date"] = from_date

            # BUILD URL QUERYSTRING
            querystring = URLQuerystringBuilder.AT_querystring_from_date(api_param)
            Session.get_current_session().debug_msg(f"{BotAtmotube.__name__}: try to build URL querystring: OK")

            # MAKE API REQUEST
            answer = self.apiadapter.fetch(querystring)
            Session.get_current_session().debug_msg(f"{BotAtmotube.__name__}: try to make API request: OK")

            # GET JSON PARSER FOR CONVERTING API ANSWER
            parser = FileParserFactory.file_parser_from_file_extension("json")
            parsed_api_answer = parser.parse(answer)
            Session.get_current_session().debug_msg(f"{BotAtmotube.__name__}: try to parse API answer: OK")

            # BUILD QUERY FOR INSERTING DATA INTO TABLES
            packets = APIPacketPicket.pick_atmotube_api_packet(parsed_api_answer = parsed_api_answer["data"]["items"],
                                                               param_id_code = id_code_dict)
            Session.get_current_session().debug_msg(f"{BotAtmotube.__name__}: try to pick API packets: OK")

            # TRY INSERT MEASUREMENT
            query = self.sqlbuilder.insert_measurement(packets)
            self.dbconn.send(query)
            Session.get_current_session().debug_msg(f"{BotAtmotube.__name__}: try to insert sensor measurements: OK")


################################ FACTORY ################################
class BotFactory(builtins.object):


    @staticmethod
    def create_bot_from_personality(bot_personality: str) -> BaseBot:

        if bot_personality == "atmotube":
            return BotAtmotube()
        else:
            raise SystemExit(f"{BotFactory.__name__}: invalid bot personality {bot_personality}.")
