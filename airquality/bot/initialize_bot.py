#################################################
#
# @Author: davidecolombo
# @Date: gio, 28-10-2021, 08:30
# @Description: this script contains the classes for initializing the database with different sensor's data.
#
#################################################
import builtins
from abc import ABC, abstractmethod

# IMPORT GLOBAL VARIABLE FROM FETCH MODULE
import airquality.constants.system_constants as sc

# IMPORT CLASSES FROM AIRQUALITY MODULE
from airquality.filter.identifier_packet_filter import IdentifierPacketFilterFactory
from airquality.database.db_conn_adapter import Psycopg2ConnectionAdapterFactory
from airquality.api.url_querystring_builder import URLQuerystringBuilderFactory
from airquality.reshaper.api_packet_reshaper import APIPacketReshaperFactory
from airquality.picker.api_packet_picker import APIPacketPickerFactory
from airquality.parser.db_answer_parser import DatabaseAnswerParser
from airquality.database.sql_query_builder import SQLQueryBuilder
from airquality.api.api_request_adapter import APIRequestAdapter
from airquality.picker.json_param_picker import JSONParamPicker
from airquality.picker.resource_picker import ResourcePicker
from airquality.parser.file_parser import FileParserFactory
from airquality.io.io import IOManager

# IMPORT SHARED CONSTANTS
from airquality.constants.shared_constants import QUERY_FILE, API_FILE, SERVER_FILE, DEBUG_HEADER, EMPTY_LIST, \
    THINGSPEAK_TIMESTAMP_1A, THINGSPEAK_TIMESTAMP_1B, THINGSPEAK_TIMESTAMP_2B, THINGSPEAK_TIMESTAMP_2A


class InitializeBot(ABC):

    @abstractmethod
    def run(self):
        pass


class InitializeBotPurpleair(InitializeBot):

    def run(self):

        ################################ READ SERVER FILE ################################
        raw_server_data = IOManager.open_read_close_file(path=SERVER_FILE)
        parser = FileParserFactory.file_parser_from_file_extension(file_extension=SERVER_FILE.split('.')[-1])
        parsed_server_data = parser.parse(raw_string=raw_server_data)

        ################################ PICK DATABASE CONNECTION PROPERTIES ################################
        db_settings = ResourcePicker.pick_db_conn_properties(parsed_resources=parsed_server_data,
                                                             bot_personality=sc.PERSONALITY)

        ################################ DATABASE CONNECTION ADAPTER ################################
        db_conn_factory = Psycopg2ConnectionAdapterFactory()
        dbconn = db_conn_factory.create_database_connection_adapter(settings=db_settings)
        dbconn.open_conn()

        ################################ SQL QUERY BUILDER ################################
        query_builder = SQLQueryBuilder(query_file_path=QUERY_FILE)

        ################################ SELECT SENSOR NAME FROM DATABASE ################################
        # The 'sensor_names' variable is used to check if a given sensor taken from the API is already present
        # into the database.
        query = query_builder.select_all_sensor_name_from_identifier(identifier=sc.PERSONALITY)
        answer = dbconn.send(executable_sql_query=query)
        sensor_names = DatabaseAnswerParser.parse_single_attribute_answer(response=answer)

        if sc.DEBUG_MODE:
            if sensor_names != EMPTY_LIST:
                for name in sensor_names:
                    print(f"{DEBUG_HEADER} name = '{name}' is already present.")
            else:
                print(f"{DEBUG_HEADER} not sensor found for personality '{sc.PERSONALITY}'.")

        ################################ SELECT THE SENSOR ID FOR THE NEXT INSERTIONS ################################
        # Since we have to insert new sensors we need some information:
        #   - the sensor already exist?
        #   - the max sensor id from the sensor table (needed as 'foreign key' for other tables)

        sensor_id = 1
        query = query_builder.select_max_sensor_id()
        answer = dbconn.send(executable_sql_query=query)
        max_sensor_id = DatabaseAnswerParser.parse_single_attribute_answer(answer)
        if max_sensor_id[0] is not None:
            if sc.DEBUG_MODE:
                print(f"{DEBUG_HEADER} found sensor in the database with id = {str(max_sensor_id[0])}.")
            sensor_id = max_sensor_id[0] + 1

        ################################ READ API FILE ################################
        raw_api_data = IOManager.open_read_close_file(path=API_FILE)
        parser = FileParserFactory.file_parser_from_file_extension(file_extension=API_FILE.split('.')[-1])
        parsed_api_data = parser.parse(raw_string=raw_api_data)

        ################################ PICK API ADDRESS FROM PARSED JSON DATA ################################
        path2key = [sc.PERSONALITY, "api_address"]
        api_address = JSONParamPicker.pick_parameter(parsed_json=parsed_api_data, path2key=path2key)
        if sc.DEBUG_MODE:
            print(20 * "=" + " API ADDRESS " + 20 * '=')
            print(f"{DEBUG_HEADER} {api_address}")

        ################################ API REQUEST ADAPTER ################################
        api_adapter = APIRequestAdapter(api_address=api_address)

        ################################ QUERYSTRING BUILDER ################################
        querystring_builder = URLQuerystringBuilderFactory.create_querystring_builder(bot_personality=sc.PERSONALITY)
        querystring = querystring_builder.make_querystring(parameters=parsed_api_data[sc.PERSONALITY])

        ################################ FETCHING API DATA ################################
        raw_api_packets = api_adapter.fetch(querystring=querystring)
        parser = FileParserFactory.file_parser_from_file_extension(file_extension='json')
        parsed_api_data = parser.parse(raw_string=raw_api_packets)

        ################ RESHAPE API DATA FOR GETTING THEM IN A BETTER SHAPE FOR DATABASE INSERTION ####################
        reshaper = APIPacketReshaperFactory().create_api_packet_reshaper(bot_personality=sc.PERSONALITY)
        reshaped_packets = reshaper.reshape_packet(api_answer=parsed_api_data)
        if sc.DEBUG_MODE:
            print(20 * "=" + " RESHAPED API PACKETS " + 20 * '=')
            for packet in reshaped_packets:
                print(30 * '*')
                for key, val in packet.items():
                    print(f"{DEBUG_HEADER} {key} = {val}")

        ########################### CREATE IDENTIFIER FILTER FOR FILTERING API PACKETS ############################
        filter_factory = IdentifierPacketFilterFactory()
        filter_ = filter_factory.create_identifier_filter(bot_personality=sc.PERSONALITY)

        ################################ FILTER API PACKETS ################################
        # Filter packets based on sensor names. This is done to avoid to insert sensors that are
        # already present in the database.

        filtered_packets = filter_.filter_packets(packets=reshaped_packets, identifiers=sensor_names)
        if sc.DEBUG_MODE:
            print(20 * "=" + " FILTERED PACKETS " + 20 * '=')
            for packet in filtered_packets:
                print(30 * '*')
                for key, val in packet.items():
                    print(f"{DEBUG_HEADER} {key} = {val}")

        ####################### IF THERE ARE NO NEW SENSORS TO ADD, RETURN FROM THE METHOD ########################
        if filtered_packets == EMPTY_LIST:
            if sc.DEBUG_MODE:
                print(f"{DEBUG_HEADER} all the sensors found are already present into the database.")
            dbconn.close_conn()
            return

        ################################ INSERT NEW SENSORS INTO THE DATABASE ################################
        query = query_builder.insert_sensors_from_identifier(packets=filtered_packets, identifier=sc.PERSONALITY)
        dbconn.send(executable_sql_query=query)

        ########## CREATE API PACKET PICKER FOR PICKING ONLY SELECTED FIELDS FROM ALL THOSE IN THE API PACKETS #########
        picker = APIPacketPickerFactory().create_api_packet_picker(bot_personality=sc.PERSONALITY)

        ################################ PICK ONLY API PARAMETERS FROM ALL PARAMETERS IN THE PACKETS ###################
        api_param2pick = ResourcePicker.pick_api_param_filter_list_from_personality(bot_personality=sc.PERSONALITY)
        new_api_packets = picker.pick_packet_params(packets=filtered_packets, param2pick=api_param2pick)

        # ADD CHANNELS TIMESTAMP VARIABLES TO UNDERSTAND WHICH IS THE LAST MEASURE FOR A GIVEN CHANNEL
        # WHEN FETCHING DATA IN FUTURE
        for packet in new_api_packets:
            packet[THINGSPEAK_TIMESTAMP_1A] = None
            packet[THINGSPEAK_TIMESTAMP_1B] = None
            packet[THINGSPEAK_TIMESTAMP_2A] = None
            packet[THINGSPEAK_TIMESTAMP_2B] = None

        if sc.DEBUG_MODE:
            print(20 * "=" + " API PARAM TABLE PACKETS " + 20 * '=')
            for packet in new_api_packets:
                print(30 * '*')
                for key, val in packet.items():
                    print(f"{DEBUG_HEADER} {key} = {val}")

        ################################ ASK THE SQL QUERY BUILDER TO BUILD THE QUERY ################################
        query = query_builder.insert_api_param(packets=new_api_packets, first_sensor_id=sensor_id)
        dbconn.send(executable_sql_query=query)

        ###################### PICK ONLY GEO PARAMETERS FROM ALL PARAMETERS IN THE PACKETS #########################
        geo_param2pick = ResourcePicker.pick_geo_param_filter_list_from_personality(personality=sc.PERSONALITY)
        new_geo_packets = picker.pick_packet_params(packets=filtered_packets, param2pick=geo_param2pick)

        ################################ INSERT THE RECORDS INTO THE DATABASE ################################
        query = query_builder.insert_sensor_at_location(packets=new_geo_packets, first_sensor_id=sensor_id)
        dbconn.send(executable_sql_query=query)

        ################################ SAFELY CLOSE DATABASE CONNECTION ################################
        dbconn.close_conn()


################################ FACTORY ################################
class InitializeBotFactory(builtins.object):

    @classmethod
    def create_initialize_bot(cls, bot_personality: str) -> InitializeBot:

        if bot_personality == "purpleair":
            return InitializeBotPurpleair()
        else:
            raise SystemExit(f"{InitializeBotFactory.__name__}: cannot instantiate {InitializeBot.__name__} "
                             f"instance for personality='{bot_personality}'.")
