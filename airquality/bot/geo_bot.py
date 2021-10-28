#################################################
#
# @Author: davidecolombo
# @Date: gio, 28-10-2021, 11:21
# @Description: this script defines the classes for running the geo bot
#
#################################################
import builtins
from abc import ABC, abstractmethod

# IMPORT GLOBAL VARIABLE FROM FETCH MODULE
import airquality.constants.system_constants as sc

# IMPORT CLASSES FROM AIRQUALITY MODULE
from airquality.reshaper.api2db_station_reshaper import API2DatabaseStationReshaperFactory
from airquality.filter.identifier_packet_filter import IdentifierPacketFilterFactory
from airquality.database.db_conn_adapter import Psycopg2ConnectionAdapterFactory
from airquality.api.url_querystring_builder import URLQuerystringBuilderFactory
from airquality.reshaper.api_packet_reshaper import APIPacketReshaperFactory
from airquality.reshaper.api2db_reshaper import API2DatabaseReshaperFactory
from airquality.reshaper.db2api_reshaper import Database2APIReshaperFactory
from airquality.parser.db_answer_parser import DatabaseAnswerParser
from airquality.keeper.packets_keeper import APIPacketKeeperFactory
from airquality.database.sql_query_builder import SQLQueryBuilder
from airquality.api.api_request_adapter import APIRequestAdapter
from airquality.picker.json_param_picker import JSONParamPicker
from airquality.picker.resource_picker import ResourcePicker
from airquality.parser.file_parser import FileParserFactory
from airquality.io.io import IOManager

# IMPORT SHARED CONSTANTS
from airquality.constants.shared_constants import QUERY_FILE, API_FILE, SERVER_FILE, DEBUG_HEADER, EMPTY_LIST


################################ GEO BOT ABSTRACT BASE CLASS ################################
class GeoBot(ABC):


    @abstractmethod
    def run(self):
        pass


class GeoBotPurpleair(GeoBot):


    def run(self):

        ################################ READ SERVER FILE ################################
        raw_server_data = IOManager.open_read_close_file(path = SERVER_FILE)
        parser = FileParserFactory.file_parser_from_file_extension(file_extension = SERVER_FILE.split('.')[-1])
        parsed_server_data = parser.parse(raw_string = raw_server_data)

        ################################ PICK DATABASE CONNECTION PROPERTIES ################################
        db_settings = ResourcePicker.pick_db_conn_properties(parsed_resources = parsed_server_data,
                                                             bot_personality = sc.PERSONALITY)
        if sc.DEBUG_MODE:
            print(20 * "=" + " DATABASE SETTINGS " + 20 * '=')
            for key, val in db_settings.items():
                print(f"{DEBUG_HEADER} {key}={val}")

        ################################ DATABASE CONNECTION ADAPTER ################################
        db_conn_factory = Psycopg2ConnectionAdapterFactory()
        dbconn = db_conn_factory.create_database_connection_adapter(settings = db_settings)
        dbconn.open_conn()

        ################################ SQL QUERY BUILDER ################################
        query_builder = SQLQueryBuilder(query_file_path = QUERY_FILE)

        ################################ SELECT SENSOR NAME FROM DATABASE ################################
        # The 'sensor_names' variable is used to check if a given sensor taken from the API is already present
        # into the database.
        query = query_builder.select_all_sensor_name_from_identifier(identifier = sc.PERSONALITY)
        answer = dbconn.send(executable_sql_query = query)
        sensor_names = DatabaseAnswerParser.parse_single_attribute_answer(response = answer)

        if sc.DEBUG_MODE:
            if sensor_names != EMPTY_LIST:
                for name in sensor_names:
                    print(f"{DEBUG_HEADER} name = '{name}' is already present.")
            else:
                print(f"{DEBUG_HEADER} not sensor found for personality '{sc.PERSONALITY}'.")

        ################################ READ API FILE ################################
        raw_api_data = IOManager.open_read_close_file(path = API_FILE)
        parser = FileParserFactory.file_parser_from_file_extension(file_extension = API_FILE.split('.')[-1])
        parsed_api_data = parser.parse(raw_string = raw_api_data)

        ################################ PICK API ADDRESS FROM PARSED JSON DATA ################################
        path2key = [sc.PERSONALITY, "api_address", sc.API_ADDRESS_N]
        api_address = JSONParamPicker.pick_parameter(parsed_json = parsed_api_data, path2key = path2key)
        if sc.DEBUG_MODE:
            print(20 * "=" + " API ADDRESS " + 20 * '=')
            print(f"{DEBUG_HEADER} {api_address}")

        ################################ API REQUEST ADAPTER ################################
        api_adapter = APIRequestAdapter(api_address = api_address)

        ################################ QUERYSTRING BUILDER ################################
        querystring_builder = URLQuerystringBuilderFactory.create_querystring_builder(bot_personality = sc.PERSONALITY)
        querystring = querystring_builder.make_querystring(parameters = parsed_api_data[sc.PERSONALITY])

        ################################ FETCHING API DATA ################################
        raw_api_packets = api_adapter.fetch(querystring = querystring)
        parser = FileParserFactory.file_parser_from_file_extension(file_extension = 'json')
        parsed_api_data = parser.parse(raw_string = raw_api_packets)

        ################ RESHAPE API DATA FOR GETTING THEM IN A BETTER SHAPE FOR DATABASE INSERTION ####################
        reshaper = APIPacketReshaperFactory().create_api_packet_reshaper(bot_personality = sc.PERSONALITY)
        reshaped_packets = reshaper.reshape_packet(api_answer = parsed_api_data)
        if sc.DEBUG_MODE:
            print(20 * "=" + " RESHAPED API PACKETS " + 20 * '=')
            for packet in reshaped_packets:
                print(30 * '*')
                for key, val in packet.items():
                    print(f"{DEBUG_HEADER} {key} = {val}")

        ####### CREATE PACKET KEEPER FOR KEEPING ONLY THOSE PACKETS FROM SENSORS ALREADY PRESENT INTO THE DATABASE ########
        keeper = APIPacketKeeperFactory().create_packet_keeper(bot_personality = sc.PERSONALITY)

        filtered_packets = keeper.keep_packets(packets = reshaped_packets, identifiers = sensor_names)
        if sc.DEBUG_MODE:
            print(20 * "=" + " FILTERED PACKETS " + 20 * '=')
            for packet in filtered_packets:
                print(30 * '*')
                for key, val in packet.items():
                    print(f"{DEBUG_HEADER} {key} = {val}")

        




#         ################################ SELECT SENSOR IDS FROM IDENTIFIER ################################
#         query = query_builder.select_sensor_ids_from_identifier(identifier = sc.PERSONALITY)
#         answer = dbconn.send(executable_sql_query = query)
#         sensor_ids = DatabaseAnswerParser.parse_single_attribute_answer(response = answer)
#
#         if sc.DEBUG_MODE:
#             print(20 * "=" + " DATABASE SENSOR IDS " + 20 * '=')
#             for id_ in sensor_ids:
#                 print(f"{DEBUG_HEADER} {id_}")
#
#         ################################ IF THERE ARE NO SENSORS, THE PROGRAM STOPS HERE ###############################
#         if sensor_ids == EMPTY_LIST:
#             if sc.DEBUG_MODE:
#                 print(f"{DEBUG_HEADER} no sensor associated to personality = '{sc.PERSONALITY}'.")
#             dbconn.close_conn()
#             return
#
# ################################ FOR EACH SENSOR DO THE STUFF BELOW ################################
#
#         for sensor_id in sensor_ids:
#
#             print(20 * "*" + f" {sensor_id} " + 20 * '*')









################################ FACTORY ################################
class GeoBotFactory(builtins.object):


    @classmethod
    def create_geo_bot(cls, bot_personality: str) -> GeoBot:

        if bot_personality == "purpleair":
            return GeoBotPurpleair()
        else:
            raise SystemExit(f"{GeoBotFactory.__name__}: cannot instantiate {GeoBot.__name__} "
                             f"instance for personality='{bot_personality}'.")
