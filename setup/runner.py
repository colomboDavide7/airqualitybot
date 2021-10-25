#################################################
#
# @Author: davidecolombo
# @Date: dom, 24-10-2021, 20:36
# @Description: this script defines the main function for the 'setup' module

#               This module is used for loading for the first time the sensor's data to the
#
#################################################
import sys
from typing import List
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


# PATH TO FILES
SETUP_FILE  = "properties/setup.json"
SERVER_FILE = "properties/server.json"
QUERY_FILE  = "properties/sql_query.json"

# DEBUG STRING HEADER
DEBUG_HEADER = "[DEBUG]:"

# USAGE STRING
USAGE = "USAGE: python -m setup [-d or --debug] personality"

# COMMAND LINE ARGUMENTS
VALID_PERSONALITIES = ('purpleair', 'atmotube')
DEBUG_MODE = False
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
        raise SystemExit(f"{parse_sys_argv.__name__}(): missing personality argument. \n{USAGE}")


def main():
    """This function is the entry point for the 'setup' module.

    The module allows to set up all the information associated to the sensors and add them to the database."""

    args = sys.argv[1:]
    if args:
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
        if not sensor_names and DEBUG_MODE:
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
        raw_setup_data = IOManager.open_read_close_file(path = SETUP_FILE)
        parser = FileParserFactory.file_parser_from_file_extension(file_extension = SETUP_FILE.split('.')[-1])
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

################################ FILTER API PACKET ################################
        filter_factory = APIPacketFilterFactory()
        api_packet_filter = filter_factory.create_api_packet_filter(bot_personality = PERSONALITY)




################################ INSERT NEW SENSORS INTO THE DATABASE ################################

        if PERSONALITY == "purpleair":
            insert_sensor_query = query_builder.insert_sensors(packets = reshaped_packets, identifier = PERSONALITY)
            if DEBUG_MODE:
                print(f"{DEBUG_HEADER} {insert_sensor_query}")

        else:
            print("I don't know what to do")



        print(20 * '-' + " PROGRAMS END SUCCESSFULLY " + 20 * '-')
    except Exception as ex:
        print(str(ex))
        if isinstance(ex, SystemExit):
            sys.exit(1)
















