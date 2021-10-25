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
from airquality.app import EMPTY_STRING, EMPTY_LIST
from airquality.io.io import IOManager
from airquality.parser.file_parser import FileParserFactory
from airquality.api.api_request_adapter import APIRequestAdapter
from airquality.api.url_querystring_builder import URLQuerystringBuilder
from airquality.database.db_conn_adapter import Psycopg2ConnectionAdapterFactory
from airquality.picker.resource_picker import ResourcePicker
from airquality.database.sql_query_builder import SQLQueryBuilder
from airquality.parser.db_answer_parser import DatabaseAnswerParser


# PATH TO FILES
SETUP_FILE  = "properties/setup.json"
SERVER_FILE = "properties/server.json"
QUERY_FILE  = "properties/sql_query.json"

# DEBUG STRING HEADER
DEBUG_HEADER = "[DEBUG]:"

# USAGE STRING
USAGE = "USAGE: python -m setup [-d or --debug] personality"

# COMMAND LINE ARGUMENTS
VALID_PERSONALITIES = 'purpleair'
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

        # TRY TO READ FILE
        raw_text = IOManager.open_read_close_file(path = SETUP_FILE)
        # if DEBUG_MODE:
        #     print(raw_text)

        # GET THE FILE PARSER
        parser = FileParserFactory.file_parser_from_file_extension(file_extension = SETUP_FILE.split('.')[-1])
        if DEBUG_MODE:
            print(DEBUG_HEADER + str(parser))

        # TRY TO PARSE FILE RAW TEXT
        parsed_setup_data = parser.parse(raw_string = raw_text)
        # if DEBUG_MODE:
        #     print(parsed_setup_data)

        # MAKE API REQUEST ADAPTER
        api_adapter = APIRequestAdapter(parsed_setup_data[f"{PERSONALITY}"]["api_address"])

        # TRY TO BUILD QUERYSTRING FROM API PARAMETERS
        querystring = URLQuerystringBuilder.PA_querystring_from_fields(api_param = parsed_setup_data[f"{PERSONALITY}"])
        if DEBUG_MODE:
            print(DEBUG_HEADER + querystring)

        # TRY TO FETCH DATA FROM PURPLE AIR API
        raw_string = api_adapter.fetch(query_string = querystring)
        # if DEBUG_MODE:
        #     print(raw_string)

        # GET JSON PARSER
        parser = FileParserFactory.file_parser_from_file_extension(file_extension = 'json')

        # TRY TO PARSE API REQUEST
        parsed_api_data = parser.parse(raw_string = raw_string)
        # if DEBUG_MODE:
        #     print(DEBUG_HEADER + str(parsed_api_data))

        # TRY TO READ SERVER FILE
        raw_server = IOManager.open_read_close_file(path = SERVER_FILE)
        # if DEBUG_MODE:
        #     print(DEBUG_HEADER + raw_server)

        # TRY TO GET PARSER FROM FILE EXTENSION
        parser = FileParserFactory.file_parser_from_file_extension(file_extension = SERVER_FILE.split('.')[-1])
        parsed_server = parser.parse(raw_string = raw_server)
        # if DEBUG_MODE:
        #     print(DEBUG_HEADER + parsed_server)

        # TRY TO PICK DATABASE CONNECTION SETTINGS FROM PARSED SERVER
        db_settings = ResourcePicker.pick_db_conn_properties_from_personality(
                parsed_resources = parsed_server,
                bot_personality = PERSONALITY)
        # if DEBUG_MODE:
        #     print(DEBUG_HEADER + str(db_settings))

        # TRY TO GET DATABASE CONNECTION ADAPTER
        db_conn_factory = Psycopg2ConnectionAdapterFactory()
        dbconn = db_conn_factory.create_database_connection_adapter(settings = db_settings)

        # TRY TO OPEN CONNECTION WITH THE DATABASE
        dbconn.open_conn()

        # TRY TO MAKE SQL QUERY BUILDER
        query_builder = SQLQueryBuilder(query_file_path = QUERY_FILE)

        # TRY TO SELECT MAX MANUFACTURER ID FROM DATABASE
        # THIS IS DONE IN ORDER TO KNOW WHAT IS THE ID ASSOCIATED TO THE NEW MANUFACTURER THAT THIS SCRIPT
        # INSERT BELOW, SINCE THE MANUFACTURER ID IS THE FOREIGN KEY IN THE 'SENSOR' TABLE.
        query = query_builder.select_max_manufacturer_id()
        answer = dbconn.send(executable_sql_query = query)
        max_manufacturer_id = DatabaseAnswerParser.parse_single_attribute_answer(answer)

        # IF THE 'MANUFACTURER' TABLE IS EMPTY, AN EMPTY LIST IS RETURNED.
        # IN THIS CASE, THE ID IS SET TO ZERO.
        if max_manufacturer_id == EMPTY_LIST:
            manufacturer_id = 1
        else:
            # INCREMENT MAX MANUFACTURER ID BY ONE, SINCE WE NEED THE ID OF OUR NEW MANUFACTURER
            manufacturer_id = max_manufacturer_id[0] + 1

        if DEBUG_MODE:
            print(DEBUG_HEADER + str(manufacturer_id))

        # TRY TO BUILD QUERY FOR INSERTING NEW MANUFACTURER INTO THE DATABASE
        query = query_builder.insert_manufacturer(personality = PERSONALITY)
        if DEBUG_MODE:
            print(DEBUG_HEADER + query)

        # TRY TO INSERT NEW MANUFACTURER INTO THE DATABASE
        # dbconn.send(executable_sql_query = query)


        # SELECT MAX SENSOR ID
        query = query_builder.select_max_sensor_id()
        answer = dbconn.send(executable_sql_query = query)
        max_sensor_id = DatabaseAnswerParser.parse_single_attribute_answer(answer)

        if max_sensor_id == EMPTY_LIST:
            sensor_id = 1
        else:
            sensor_id = max_sensor_id[0] + 1

        # TRY TO INSERT ALL THE SENSORS
        # for sensor_data in parsed_api_data["data"]:
        #     sensor_id += 1
        #     print(20*'*' + f" SENSOR {sensor_id}" + 20*'*')
        #     for i in range(len(sensor_data)):
        #         print(parsed_api_data["fields"][i] + " = " + str(sensor_data[i]))



        print(20 * '-' + " PROGRAMS END SUCCESSFULLY " + 20 * '-')
    except Exception as ex:
        print(str(ex))
        if isinstance(ex, SystemExit):
            sys.exit(1)
















