#################################################
#
# @Author: davidecolombo
# @Date: lun, 18-10-2021, 12:29
# @Description: this script defines the functions for parsing application arguments and 'main()'.
#
#################################################
import sys
from typing import List
from airquality.io.io import IOManager
from airquality.picker.json_param_picker import JSONParamPicker
from airquality.picker.resource_picker import ResourcePicker
from airquality.api.api_request_adapter import APIRequestAdapter
from airquality.database.sql_query_builder import SQLQueryBuilder
from airquality.database.db_conn_adapter import Psycopg2ConnectionAdapterFactory
from airquality.parser.db_answer_parser import DatabaseAnswerParser
from airquality.api.url_querystring_builder import URLQuerystringBuilderFactory
from airquality.parser.file_parser import FileParserFactory
from airquality.reshaper.api2db_reshaper import API2DatabaseReshaperFactory
from airquality.filter.datetime_packet_filter import DatetimePacketFilterFactory
from airquality.constants.shared_constants import FETCH_USAGE, VALID_PERSONALITIES, DEBUG_HEADER, \
    SERVER_FILE, QUERY_FILE, API_FILE, MOBILE_SENSOR_PERSONALITIES, EMPTY_LIST


DEBUG_MODE = False
PERSONALITY = ""
API_ADDRESS_N = ""


def parse_sys_argv(args: List[str]):

    global DEBUG_MODE
    global PERSONALITY
    global API_ADDRESS_N

    if args[0] in ("--help", "-h"):
        print(FETCH_USAGE)
        sys.exit(0)

    is_personality_set = False
    is_api_address_number_set = False

    for arg in args:
        if arg in ("-d", "--debug"):
            DEBUG_MODE = True
        elif not is_personality_set and arg in VALID_PERSONALITIES:
            PERSONALITY = arg
            is_personality_set = True
        elif not is_api_address_number_set and arg.isdigit():
            API_ADDRESS_N = arg
            is_api_address_number_set = True
        else:
            print(f"{parse_sys_argv.__name__}: ignore invalid option '{arg}'.")

    if not is_personality_set:
        raise SystemExit(f"{parse_sys_argv.__name__}(): missing required bot personality.")

    if not is_api_address_number_set:
        raise SystemExit(f"{parse_sys_argv.__name__}(): missing required api address number.")


################################ MAIN FUNCTION ################################
def main() -> None:
    """This function is the entry point for the application

    {usage}

    The application expects two optional command line option-argument:
    1) --help or -h:  display help on program usage (MUST BE THE FIRST)
    2) --debug or -d: run the application in debug mode
    3) personality:   the bot personality for connecting to APIs and database
    4) api address number: the api address number from the 'api_address' section in the resource file
    """.format(usage = FETCH_USAGE)

    args = sys.argv[1:]
    if not args:
        print(FETCH_USAGE)
        sys.exit(1)

    parse_sys_argv(args)
    print(f"{DEBUG_HEADER} personality = {PERSONALITY}")
    print(f"{DEBUG_HEADER} api address number = {API_ADDRESS_N}")
    print(f"{DEBUG_HEADER} debug       = {DEBUG_MODE}")

    try:
        print(20 * '-' + " START THE PROGRAM " + 20 * '-')

################################ READ SERVER FILE ################################
        raw_server_data = IOManager.open_read_close_file(path = SERVER_FILE)
        parser = FileParserFactory.file_parser_from_file_extension(file_extension = SERVER_FILE.split('.')[-1])
        parsed_server_data = parser.parse(raw_string = raw_server_data)

################################ PICK DATABASE CONNECTION PROPERTIES ################################
        db_settings = ResourcePicker.pick_db_conn_properties(parsed_resources = parsed_server_data,
                                                             bot_personality = PERSONALITY)
        if DEBUG_MODE:
            print(20 * "=" + " DATABASE SETTINGS " + 20 * '=')
            for key, val in db_settings.items():
                print(f"{DEBUG_HEADER} {key}={val}")

################################ DATABASE CONNECTION ADAPTER ################################
        db_conn_factory = Psycopg2ConnectionAdapterFactory()
        dbconn = db_conn_factory.create_database_connection_adapter(settings = db_settings)
        dbconn.open_conn()

################################ SQL QUERY BUILDER ################################
        query_builder = SQLQueryBuilder(query_file_path = QUERY_FILE)

################################ READ API FILE ################################
        raw_setup_data = IOManager.open_read_close_file(path = API_FILE)
        parser = FileParserFactory.file_parser_from_file_extension(file_extension = API_FILE.split('.')[-1])
        parsed_api_data = parser.parse(raw_string = raw_setup_data)

################################ PICK API ADDRESS FROM PARSED JSON DATA ################################
        path2key = [PERSONALITY, "api_address", API_ADDRESS_N]
        api_address = JSONParamPicker.pick_parameter(parsed_json = parsed_api_data, path2key = path2key)
        if DEBUG_MODE:
            print(20 * "=" + " API ADDRESS " + 20 * '=')
            print(f"{DEBUG_HEADER} {api_address}")


################################ API REQUEST ADAPTER ################################
        api_adapter = APIRequestAdapter(api_address = api_address)

################################ SELECT SENSOR IDS FROM IDENTIFIER ################################
        query = query_builder.select_sensor_ids_from_identifier(identifier = PERSONALITY)
        answer = dbconn.send(executable_sql_query = query)
        sensor_ids = DatabaseAnswerParser.parse_single_attribute_answer(response = answer)

        if DEBUG_MODE:
            print(20 * "=" + " DATABASE SENSOR IDS " + 20 * '=')
            for id_ in sensor_ids:
                print(f"{DEBUG_HEADER} {id_}")

################################ IF THERE ARE NO SENSORS, THE PROGRAM STOPS HERE ################################
        if sensor_ids == EMPTY_LIST:
            print(f"{DEBUG_HEADER} no sensor associated to personality = '{PERSONALITY}'.")
            sys.exit(0)

################################ SELECT MEASURE PARAM FROM IDENTIFIER ################################
        query = query_builder.select_measure_param_from_identifier(identifier = PERSONALITY)
        answer = dbconn.send(executable_sql_query = query)
        measure_param_map = DatabaseAnswerParser.parse_key_val_answer(answer)

        if DEBUG_MODE:
            print(20 * "=" + " MEASURE PARAM MAPPING " + 20 * '=')
            for code, id_ in measure_param_map.items():
                print(f"{DEBUG_HEADER} {code}={id_}")


################################ FOR EACH SENSOR DO THE STUFF BELOW ################################

        for sensor_id in sensor_ids:

            print(20 * "*" + f" {sensor_id} " + 20 * '*')

            ################################ SELECT SENSOR API PARAM FROM DATABASE ################################
            query = query_builder.select_sensor_api_param(sensor_id = sensor_id)
            answer = dbconn.send(executable_sql_query = query)
            api_param = DatabaseAnswerParser.parse_key_val_answer(answer)

            if DEBUG_MODE:
                print(20 * "=" + " API PARAMETERS " + 20 * '=')
                for name, value in api_param.items():
                    print(f"{DEBUG_HEADER} {name}={value}")

            ################################ DO THE STUFF BELOW ONLY FOR MOBILE SENSORS ################################
            if PERSONALITY in MOBILE_SENSOR_PERSONALITIES:

                ################################ BUILD URL QUERYSTRING FROM API PARAM ################################
                querystring_builder = URLQuerystringBuilderFactory.create_querystring_builder(bot_personality = PERSONALITY)
                querystring = querystring_builder.make_querystring(parameters = api_param)

                if DEBUG_MODE:
                    print(20 * "=" + " URL QUERYSTRING " + 20 * '=')
                    print(f"{DEBUG_HEADER} {querystring}")

                ################################ FETCH DATA FROM API ################################
                api_answer = api_adapter.fetch(querystring = querystring)
                parser = FileParserFactory.file_parser_from_file_extension(file_extension = "json")
                api_answer = parser.parse(raw_string = api_answer)

                ################################ FILTER PACKETS FROM LAST TIMESTAMP ON ################################
                filter_sqltimestamp = ResourcePicker.pick_last_timestamp_from_api_param_by_personality(api_param = api_param,
                                                                                                       personality = PERSONALITY)
                filter_ = DatetimePacketFilterFactory().create_datetime_filter(bot_personality = PERSONALITY)
                filtered_packets = filter_.filter_packets(packets = api_answer, sqltimestamp = filter_sqltimestamp)

                if DEBUG_MODE:
                    print(20 * "=" + " FILTERED PACKETS " + 20 * '=')
                    if filtered_packets != EMPTY_LIST:
                        for i in range(10):
                            rpacket = filtered_packets[i]
                            for key, val in rpacket.items():
                                print(f"{DEBUG_HEADER} {key}={val}")

################################ INSERT NEW MEASURE ONLY IF THERE ARE NEW MEASURE ################################

                if filtered_packets != EMPTY_LIST:


                    ################################ RESHAPE API PACKET FOR INSERT MEASURE IN DATABASE #####################
                    reshaper = API2DatabaseReshaperFactory().create_api2database_reshaper(bot_personality = PERSONALITY)
                    reshaped_packets = reshaper.reshape_packets(packets = filtered_packets,
                                                                measure_param_map = measure_param_map)

                    if DEBUG_MODE:
                        print(20 * "=" + " RESHAPED PACKETS " + 20 * '=')
                        if reshaped_packets != EMPTY_LIST:
                            for i in range(10):
                                rpacket = reshaped_packets[i]
                                for key, val in rpacket.items():
                                    print(f"{DEBUG_HEADER} {key}={val}")

                    ################################ CREATE QUERY FOR INSERTING SENSOR MEASURE TO DATABASE #################
                    query = query_builder.insert_atmotube_measurements(reshaped_packets)
                    dbconn.send(executable_sql_query = query)

                    ############### UPDATE LAST MEASURE TIMESTAMP FOR KNOWING WHERE TO START WITH NEXT FETCH ###############
                    if DEBUG_MODE:
                        print(f"{DEBUG_HEADER} last timestamp = {reshaped_packets[-1]['ts']}")

                    query = query_builder.update_last_packet_date_atmotube(last_timestamp = reshaped_packets[-1]["ts"],
                                                                           sensor_id = sensor_id)
                    dbconn.send(executable_sql_query = query)


            ################################ CODE IMPLEMENTED FOR POLLUTION STATIONS ################################
            else:
                print(f"fetching for pollution station is already not implemented.")
                sys.exit(0)


        print(20 * '-' + " PROGRAMS END SUCCESSFULLY " + 20 * '-')

    except SystemExit as ex:
        print(str(ex))
        sys.exit(1)
