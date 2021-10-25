#################################################
#
# @Author: davidecolombo
# @Date: dom, 24-10-2021, 20:36
# @Description: this script defines the main function for the 'initialize' module

#               This module is used for loading for the first time the sensor's data to the
#
#################################################
import sys
from typing import List

from airquality.constants.shared_constants import \
    SENSOR_AT_LOCATION_PERSONALITIES, VALID_PERSONALITIES, \
    API_FILE, SERVER_FILE, QUERY_FILE, \
    DEBUG_HEADER, INITIALIZE_USAGE

from airquality.app import EMPTY_LIST
from airquality.io.io import IOManager
from airquality.reshaper.reshaper import APIPacketReshaperFactory
from airquality.parser.file_parser import FileParserFactory
from airquality.api.api_request_adapter import APIRequestAdapter
from airquality.api.url_querystring_builder import URLQuerystringBuilderFactory
from airquality.database.db_conn_adapter import Psycopg2ConnectionAdapterFactory
from airquality.picker.resource_picker import ResourcePicker
from airquality.database.sql_query_builder import SQLQueryBuilder
from airquality.parser.db_answer_parser import DatabaseAnswerParser
from airquality.filter.filter import APIPacketFilterFactory


DEBUG_MODE  = False
PERSONALITY = ""


def parse_sys_argv(args: List[str]):

    global DEBUG_MODE
    global PERSONALITY
    is_personality_set = False

    for arg in args:
        if arg in ("-d", "--debug"):
            DEBUG_MODE = True
        elif arg in VALID_PERSONALITIES and not is_personality_set:
            PERSONALITY = arg
            is_personality_set = True
        else:
            print(f"{parse_sys_argv.__name__}(): ignoring invalid option '{arg}'")

    if not is_personality_set:
        raise SystemExit(f"{parse_sys_argv.__name__}(): missing personality argument. \n{INITIALIZE_USAGE}")


def main():
    """This function is the entry point for the 'initialize' module.

    The module allows to set up all the information associated to the sensors and add them to the database."""

    args = sys.argv[1:]
    if not args:
        raise SystemExit(f"{main.__name__}: missing required argument. {INITIALIZE_USAGE}")

    parse_sys_argv(args)
    print(f"{DEBUG_HEADER} personality = {PERSONALITY}")
    print(f"{DEBUG_HEADER} debug       = {DEBUG_MODE}")

    try:
        print(20*'-' + " START THE PROGRAM " + 20*'-')

################################ READ 'SERVER' FILE ################################
        raw_server_data = IOManager.open_read_close_file(path = SERVER_FILE)
        parser = FileParserFactory.file_parser_from_file_extension(file_extension = SERVER_FILE.split('.')[-1])
        parsed_server_data = parser.parse(raw_string = raw_server_data)

################################ PICK DATABASE CONNECTION PROPERTIES ################################
        db_settings = ResourcePicker.pick_db_conn_properties(parsed_resources = parsed_server_data, bot_personality = PERSONALITY)

################################ DATABASE CONNECTION ADAPTER ################################
        db_conn_factory = Psycopg2ConnectionAdapterFactory()
        dbconn = db_conn_factory.create_database_connection_adapter(settings = db_settings)
        dbconn.open_conn()

################################ SQL QUERY BUILDER ################################
        query_builder = SQLQueryBuilder(query_file_path = QUERY_FILE)

################################ SELECT SENSOR NAME FROM DATABASE ################################
        # The 'name_id_dict' variable is used to check if a given sensor taken from the API is already present
        # into the database.
        query = query_builder.select_sensor_name(identifier = PERSONALITY)
        answer = dbconn.send(executable_sql_query = query)
        sensor_names = DatabaseAnswerParser.parse_single_attribute_answer(response = answer)

        if DEBUG_MODE:
            if sensor_names:
                for name in sensor_names:
                    print(f"{DEBUG_HEADER} name = '{name}' is already present.")
            else:
                print(f"{DEBUG_HEADER} no sensor corresponding to '{PERSONALITY}' personality.")



################################ SELECT THE SENSOR ID FOR THE NEXT INSERTIONS ################################
        # Since we have to insert new sensors we need some information:
        #   - the sensor already exist?
        #   - the max sensor id from the sensor table (needed as 'foreign key' for other tables)

        sensor_id = 1
        query = query_builder.select_max_sensor_id()
        answer = dbconn.send(executable_sql_query = query)
        max_sensor_id = DatabaseAnswerParser.parse_single_attribute_answer(answer)
        if max_sensor_id != EMPTY_LIST:
            if DEBUG_MODE:
                print(f"{DEBUG_HEADER} found sensor in the database with id = {str(max_sensor_id[0])}.")
            sensor_id = max_sensor_id[0] + 1




################################ READ 'SETUP' FILE ################################
        raw_setup_data = IOManager.open_read_close_file(path = API_FILE)
        parser = FileParserFactory.file_parser_from_file_extension(file_extension = API_FILE.split('.')[-1])
        parsed_setup_data = parser.parse(raw_string = raw_setup_data)

################################ API REQUEST ADAPTER ################################
        api_adapter = APIRequestAdapter(parsed_setup_data[f"{PERSONALITY}"]["api_address"])

################################ QUERYSTRING BUILDER ################################
        querystring_builder = URLQuerystringBuilderFactory.create_querystring_builder(bot_personality = PERSONALITY)
        querystring = querystring_builder.make_querystring(parameters = parsed_setup_data[f"{PERSONALITY}"])
        if DEBUG_MODE:
            print(f"{DEBUG_HEADER} {querystring}")

################################ FETCHING API DATA ################################
        raw_api_data = api_adapter.fetch(query_string = querystring)
        parser = FileParserFactory.file_parser_from_file_extension(file_extension = 'json')
        parsed_api_data = parser.parse(raw_string = raw_api_data)

################################ RESHAPE API DATA ################################
        reshaper_factory = APIPacketReshaperFactory()
        reshaper = reshaper_factory.create_api_packet_reshaper(bot_personality = PERSONALITY)
        reshaped_packets = reshaper.reshape_packet(parsed_api_answer = parsed_api_data)
        if DEBUG_MODE:
            print(20 * "=" + " RESHAPED PACKETS " + 20 * '=')
            for packet in reshaped_packets:
                print(30*'*')
                for key, val in packet.items():
                    print(f"{DEBUG_HEADER} {key} = {val}")

################################ FILTER API PACKET ################################
        # Filter packets based on sensor names. This is done to avoid to insert sensors that are
        # already present in the database.
        filter_factory = APIPacketFilterFactory()
        api_packet_filter = filter_factory.create_api_packet_filter(bot_personality = PERSONALITY)
        filtered_packets = api_packet_filter.filter_packet(packets = reshaped_packets, filter_list = sensor_names)
        if DEBUG_MODE:
            print(20*"=" + " FILTERED PACKETS " + 20*'=')
            for packet in filtered_packets:
                print(30*'*')
                for key, val in packet.items():
                    print(f"{DEBUG_HEADER} {key} = {val}")

################################ INSERT NEW SENSORS INTO THE DATABASE ################################
        insert_sensor_query = query_builder.insert_sensors(packets = filtered_packets, identifier = PERSONALITY)
        dbconn.send(executable_sql_query = insert_sensor_query)

################################ INSERT API PARAM FOR SENSORS ################################
        insert_api_param = query_builder.insert_api_param(
                packets = filtered_packets,
                identifier = PERSONALITY,
                first_sensor_id = sensor_id)
        dbconn.send(executable_sql_query = insert_api_param)

################################ IF FIX SENSOR INSERT ALSO SENSOR AT LOCATION ################################
        if PERSONALITY in SENSOR_AT_LOCATION_PERSONALITIES:
            insert_sensor_at_location = query_builder.insert_sensor_at_location(
                    packets = filtered_packets,
                    identifier = PERSONALITY,
                    first_sensor_id = sensor_id
            )
            dbconn.send(executable_sql_query = insert_sensor_at_location)


        print(20 * '-' + " PROGRAMS END SUCCESSFULLY " + 20 * '-')
    except Exception as ex:
        print(str(ex))
        if isinstance(ex, SystemExit):
            sys.exit(1)
