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
    VALID_PERSONALITIES, \
    API_FILE, SERVER_FILE, QUERY_FILE, \
    DEBUG_HEADER, INITIALIZE_USAGE, \
    EMPTY_LIST

from airquality.io.io import IOManager
from airquality.picker.api_packet_picker import APIPacketPickerFactory
from airquality.reshaper.api_packet_reshaper import APIPacketReshaperFactory
from airquality.parser.file_parser import FileParserFactory
from airquality.api.api_request_adapter import APIRequestAdapter
from airquality.api.url_querystring_builder import URLQuerystringBuilderFactory
from airquality.database.db_conn_adapter import Psycopg2ConnectionAdapterFactory
from airquality.database.sql_query_builder import SQLQueryBuilder
from airquality.parser.db_answer_parser import DatabaseAnswerParser
from airquality.filter.identifier_packet_filter import IdentifierPacketFilterFactory
from airquality.picker.resource_picker import ResourcePicker


DEBUG_MODE  = False
PERSONALITY = ""
API_ADDRESS_N = ""


def parse_sys_argv(args: List[str]):

    global DEBUG_MODE
    global PERSONALITY
    global API_ADDRESS_N

    is_personality_set = False
    is_api_address_number_set = False

    for arg in args:
        if arg in ("-d", "--debug"):
            DEBUG_MODE = True
        elif arg in VALID_PERSONALITIES and not is_personality_set:
            PERSONALITY = arg
            is_personality_set = True
        elif arg.isdigit() and not is_api_address_number_set:
            API_ADDRESS_N = arg
            is_api_address_number_set = True
        else:
            print(f"{parse_sys_argv.__name__}(): ignoring invalid option '{arg}'")

    if not is_personality_set:
        raise SystemExit(f"{parse_sys_argv.__name__}(): missing personality argument. \n{INITIALIZE_USAGE}")

    if not is_api_address_number_set:
        raise SystemExit(f"{parse_sys_argv.__name__}(): missing required api address number.")


################################ MAIN FUNCTION INITIALIZE MODULE ################################
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

################################ READ SERVER FILE ################################
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
        # The 'sensor_names' variable is used to check if a given sensor taken from the API is already present
        # into the database.
        query = query_builder.select_all_sensor_name_from_identifier(identifier = PERSONALITY)
        answer = dbconn.send(executable_sql_query = query)
        sensor_names = DatabaseAnswerParser.parse_single_attribute_answer(response = answer)

        if DEBUG_MODE:
            if sensor_names:
                for name in sensor_names:
                    print(f"{DEBUG_HEADER} name = '{name}' is already present.")
            else:
                print(f"{DEBUG_HEADER} found {len(sensor_names)} sensors corresponding to '{PERSONALITY}' personality.")


################################ SELECT THE SENSOR ID FOR THE NEXT INSERTIONS ################################
        # Since we have to insert new sensors we need some information:
        #   - the sensor already exist?
        #   - the max sensor id from the sensor table (needed as 'foreign key' for other tables)

        sensor_id = 1
        query = query_builder.select_max_sensor_id()
        answer = dbconn.send(executable_sql_query = query)
        max_sensor_id = DatabaseAnswerParser.parse_single_attribute_answer(answer)
        if max_sensor_id[0] is not None:
            if DEBUG_MODE:
                print(f"{DEBUG_HEADER} found sensor in the database with id = {str(max_sensor_id[0])}.")
            sensor_id = max_sensor_id[0] + 1




################################ READ API FILE ################################
        raw_setup_data = IOManager.open_read_close_file(path = API_FILE)
        parser = FileParserFactory.file_parser_from_file_extension(file_extension = API_FILE.split('.')[-1])
        parsed_api_data = parser.parse(raw_string = raw_setup_data)

################################ API REQUEST ADAPTER ################################
        api_adapter = APIRequestAdapter(parsed_api_data[PERSONALITY]['api_address'][API_ADDRESS_N])

################################ QUERYSTRING BUILDER ################################
        querystring_builder = URLQuerystringBuilderFactory.create_querystring_builder(bot_personality = PERSONALITY)
        querystring = querystring_builder.make_querystring(parameters = parsed_api_data[PERSONALITY])
        if DEBUG_MODE:
            print(f"{DEBUG_HEADER} {querystring}")

################################ FETCHING API DATA ################################
        raw_api_data = api_adapter.fetch(querystring = querystring)
        parser = FileParserFactory.file_parser_from_file_extension(file_extension = 'json')
        parsed_api_data = parser.parse(raw_string = raw_api_data)

################################ RESHAPE API DATA ################################
        reshaper_factory = APIPacketReshaperFactory()
        reshaper = reshaper_factory.create_api_packet_reshaper(bot_personality = PERSONALITY)
        reshaped_packets = reshaper.reshape_packet(api_answer = parsed_api_data)
        if DEBUG_MODE:
            print(20 * "=" + " RESHAPED PACKETS " + 20 * '=')
            for packet in reshaped_packets:
                print(30*'*')
                for key, val in packet.items():
                    print(f"{DEBUG_HEADER} {key} = {val}")

################################ CREATE IDENTIFIER FILTER FOR FILTERING PACKETS FROM API ################################
        filter_factory = IdentifierPacketFilterFactory()
        filter_ = filter_factory.create_identifier_filter(bot_personality = PERSONALITY)


################################ FILTER API PACKET ################################
        # Filter packets based on sensor names. This is done to avoid to insert sensors that are
        # already present in the database.
        filtered_packets = filter_.filter_packets(packets = reshaped_packets, identifiers = sensor_names)
        if DEBUG_MODE:
            print(20*"=" + " FILTERED PACKETS " + 20*'=')
            for packet in filtered_packets:
                print(30*'*')
                for key, val in packet.items():
                    print(f"{DEBUG_HEADER} {key} = {val}")

################################ IF THERE ARE NO NEW SENSORS TO ADD, STOP THE PROGRAM ################################
        if filtered_packets == EMPTY_LIST:
            if DEBUG_MODE:
                print(f"{DEBUG_HEADER} all the sensors found are already present into the database.")
                sys.exit(0)

################################ INSERT NEW SENSORS INTO THE DATABASE ################################
        insert_sensor_query = query_builder.insert_sensors_from_identifier(packets = filtered_packets, identifier = PERSONALITY)
        dbconn.send(executable_sql_query = insert_sensor_query)

################################ INSERT API PARAM FOR SENSORS ################################

        ################################ CREATE NEW API PACKET PICKER ################################
        picker_factory = APIPacketPickerFactory()
        picker = picker_factory.create_api_packet_picker(bot_personality = PERSONALITY)

        ################################ PICK ONLY API PARAMETERS FROM ALL PARAMETERS IN THE PACKETS ###################
        api_param2pick = ResourcePicker.pick_api_param_filter_list_from_personality(bot_personality = PERSONALITY)
        new_api_packets = picker.pick_packet_params(packets = filtered_packets, param2pick = api_param2pick)

        ################################ ASK THE SQL QUERY BUILDER TO BUILD THE QUERY ################################
        query = query_builder.insert_api_param(packets = new_api_packets, first_sensor_id = sensor_id)
        dbconn.send(executable_sql_query = query)

################################ IF FIX SENSOR INSERT ALSO SENSOR AT LOCATION ################################
        # if PERSONALITY in SENSOR_AT_LOCATION_PERSONALITIES:
        #
        #     ###################### PICK ONLY GEO PARAMETERS FROM ALL PARAMETERS IN THE PACKETS #########################
        #     geo_param2pick = ResourcePicker.pick_geo_param_filter_list_from_personality(personality = PERSONALITY)
        #     new_geo_packets = picker.pick_packet_params(packets = filtered_packets, param2pick = geo_param2pick)
        #
        #     ################################ INSERT THE RECORDS INTO THE DATABASE ################################
        #     query = query_builder.insert_sensor_at_location(packets = new_geo_packets, first_sensor_id = sensor_id)
        #     dbconn.send(executable_sql_query = query)


################################ CLOSE DATABASE CONNECTION ################################
        dbconn.close_conn()

        print(20 * '-' + " PROGRAMS END SUCCESSFULLY " + 20 * '-')
    except Exception as ex:
        print(str(ex))
        if isinstance(ex, SystemExit):
            sys.exit(1)
