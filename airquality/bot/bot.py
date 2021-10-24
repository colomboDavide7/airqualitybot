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
from airquality.picker.api_packet_picker import APIPacketPicker
from airquality.parser.datetime_parser import DatetimeParser
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

            # TRY TO PICK LAST ATMOTUBE TIMESTAMP FROM API PARAMETERS
            last_atmotube_timestamp = APIPacketPicker.pick_last_atmotube_measure_timestamp_from_api_param(api_param)
            Session.get_current_session().debug_msg(f"{BotAtmotube.__name__}: try to pick last atmotube timestamp: OK")

            # TRY TO GET LAST ATMOTUBE MEASURE TIMESTAMP
            last_date = ""
            last_time = ""
            if last_atmotube_timestamp != "":
                last_date, last_time = DatetimeParser.split_last_atmotube_measure_timestamp_from_api_param(last_atmotube_timestamp)
            api_param["date"] = last_date
            Session.get_current_session().debug_msg(f"{BotAtmotube.__name__}: try to get last measure timestamp: OK")

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

            # BUILD ATMOTUBE MEASURE PACKET FOR INSERTING DATA INTO TABLES
            if last_time == "":
                packets = APIPacketPicker.pick_atmotube_api_packet(
                        parsed_api_answer = parsed_api_answer["data"]["items"],
                        param_id_code = id_code_dict
                )
            else:
                packets = APIPacketPicker.pick_atmotube_api_packets_with_timestamp_offset(
                        parsed_api_answer = parsed_api_answer["data"]["items"],
                        param_id_code = id_code_dict,
                        timestamp_offset = last_atmotube_timestamp
                )
            Session.get_current_session().debug_msg(f"{BotAtmotube.__name__}: try to pick API packets: OK")

            # TRY TO BUILD QUERY FOR INSERTING MEASUREMENT INTO DATABASE
            query = self.sqlbuilder.insert_measurements(packets)
            self.dbconn.send(query)
            Session.get_current_session().debug_msg(f"{BotAtmotube.__name__}: try to insert sensor measurements: OK")

            # UPDATE LAST TIMESTAMP FROM PACKETS
            last_timestamp = DatetimeParser.last_timestamp_from_packets(packets = packets)
            query = self.sqlbuilder.update_last_packet_date_atmotube(last_timestamp = last_timestamp, sensor_id = sensor_id)
            self.dbconn.send(query)
            Session.get_current_session().debug_msg(f"{BotAtmotube.__name__}: try to update last acquisition timestamp: OK")


################################ FACTORY ################################
class BotFactory(builtins.object):


    @staticmethod
    def create_bot_from_personality(bot_personality: str) -> BaseBot:

        if bot_personality == "atmotube":
            return BotAtmotube()
        else:
            raise SystemExit(f"{BotFactory.__name__}: invalid bot personality {bot_personality}.")
