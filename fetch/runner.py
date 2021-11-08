#################################################
#
# @Author: davidecolombo
# @Date: lun, 18-10-2021, 12:29
# @Description: this script defines the functions for parsing application arguments and 'main()'.
#
#################################################
import sys
import time
from typing import List
from airquality.bot.date_fetch_bot import DateFetchBot
from airquality.bot.fetch_bot import FetchBot

import airquality.constants.system_constants as sc

# IMPORT CLASSES FROM AIRQUALITY MODULE
from airquality.io.io import IOManager
from airquality.bot.geo_bot import GeoBot
from airquality.picker.query_picker import QueryPicker
from airquality.api.url_builder import URLBuilderPurpleair
from airquality.picker.resource_picker import ResourcePicker
from airquality.parser.db_answer_parser import DatabaseAnswerParser
from airquality.adapter.geom_adapter import GeometryAdapterPurpleair
from airquality.reshaper.packet_reshaper import PurpleairPacketReshaper
from airquality.adapter.universal_adapter import PurpleairUniversalAdapter
from airquality.parser.file_parser import FileParserFactory, JSONFileParser
from airquality.database.db_conn_adapter import Psycopg2ConnectionAdapterFactory
from airquality.container.sql_container import GeoSQLContainer, SQLContainerComposition

# IMPORT SHARED CONSTANTS
from airquality.constants.shared_constants import QUERY_FILE, API_FILE, SERVER_FILE, \
    DEBUG_HEADER, INFO_HEADER, EXCEPTION_HEADER, \
    FETCH_USAGE, VALID_PERSONALITIES


def parse_sys_argv(args: List[str]):

    if args[0] in ("--help", "-h"):
        print(FETCH_USAGE)
        sys.exit(0)

    is_personality_set = False

    for arg in args:
        if arg in ("-d", "--debug"):
            sc.DEBUG_MODE = True
        elif not is_personality_set and arg in VALID_PERSONALITIES:
            sc.PERSONALITY = arg
            is_personality_set = True
        else:
            print(f"{parse_sys_argv.__name__}: ignore invalid option '{arg}'.")

    if not is_personality_set:
        raise SystemExit(f"{parse_sys_argv.__name__}(): missing required bot personality.")


################################ MAIN FUNCTION ################################
def main():

    args = sys.argv[1:]
    if not args:
        print(FETCH_USAGE)
        sys.exit(1)

    parse_sys_argv(args)
    print(f"{INFO_HEADER} personality = {sc.PERSONALITY}")
    print(f"{INFO_HEADER} debug       = {sc.DEBUG_MODE}")

    try:
        print(20 * '-' + " START THE PROGRAM " + 20 * '-')
        start_time = time.perf_counter()

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

        ################################ READ QUERY FILE ###############################
        raw_query_data = IOManager.open_read_close_file(path=QUERY_FILE)
        parser = FileParserFactory.file_parser_from_file_extension(file_extension=QUERY_FILE.split('.')[-1])
        parsed_query_data = parser.parse(raw_string=raw_query_data)

        ################################ CREATE QUERY PICKER ###############################
        query_picker = QueryPicker(parsed_query_data)

        ################################ READ API FILE ################################
        raw_api_data = IOManager.open_read_close_file(path=API_FILE)
        parser = FileParserFactory.file_parser_from_file_extension(file_extension=API_FILE.split('.')[-1])
        parsed_api_data = parser.parse(raw_string=raw_api_data)

        ################################ GET THE API ADDRESS ################################
        try:
            api_address = parsed_api_data[sc.PERSONALITY]['api_address']
            url_param = parsed_api_data[sc.PERSONALITY]['url_param']
        except KeyError as ke:
            raise SystemExit(f"{EXCEPTION_HEADER} bad 'api.json' file structure => missing key={ke!s} "
                             f"for personality='{sc.PERSONALITY}'.")

        ################################ DATABASE SENSOR ID ASSOCIATED TO PERSONALITY ################################
        query = query_picker.select_sensor_ids_from_personality(personality=sc.PERSONALITY)
        answer = dbconn.send(executable_sql_query=query)
        sensor_ids = DatabaseAnswerParser.parse_single_attribute_answer(response=answer)

        if not sensor_ids:
            print(f"{INFO_HEADER} no sensor found for personality='{sc.PERSONALITY}'.")
            dbconn.close_conn()
            return

        if sc.DEBUG_MODE:
            print(20 * "=" + " DATABASE SENSORS ID " + 20 * '=')
            for sensor_id in sensor_ids:
                print(f"{DEBUG_HEADER} {sensor_id}")

        ################################ SELECT MEASURE PARAM FROM PERSONALITY ################################
        query = query_picker.select_measure_param_from_personality(personality=sc.PERSONALITY)
        answer = dbconn.send(executable_sql_query=query)
        measure_param_map = DatabaseAnswerParser.parse_key_val_answer(answer)
        if sc.DEBUG_MODE:
            print(20 * "=" + " MEASURE PARAM MAPPING " + 20 * '=')
            for param_code, param_id in measure_param_map.items():
                print(f"{DEBUG_HEADER} {param_code}={param_id}")

        ################################ QUERY STATEMENT ################################
        select_apiparam_query = query_picker.select_api_param_from_sensor_id()

        ############################# CREATE THE PROPER BOT OBJECT ###########################
        if sc.PERSONALITY == 'atmotube':

            # Check if the format argument exists
            if url_param.get('format') is None:
                raise SystemExit(f"{EXCEPTION_HEADER} bad 'api.json' file structure => missing 'format' key.")

            # Decide the format to use
            if url_param['format'] == 'json':
                file_parser_class = JSONFileParser
            else:
                raise SystemExit(f"{EXCEPTION_HEADER} format='{url_param['format']}' is unsupported for "
                                 f"personality='{sc.PERSONALITY}'.")
            print(f"{INFO_HEADER} using '{file_parser_class.__name__}' file parser.")

            # Decide the bot class to use
            bot_class = FetchBot
            if url_param.get('date') is not None:
                bot_class = DateFetchBot
            print(f"{INFO_HEADER} using '{bot_class.__name__}' bot.")

        # *****************************************************************
        elif sc.PERSONALITY == 'thingspeak':

            # Check if the format argument exists
            if url_param.get('format') is None:
                raise SystemExit(f"{EXCEPTION_HEADER} bad 'api.json' file structure => missing 'format' key.")

            # Decide the format to use
            if url_param['format'] == 'json':
                file_parser_class = JSONFileParser
            else:
                raise SystemExit(f"{EXCEPTION_HEADER} format='{url_param['format']}' is unsupported for "
                                 f"personality='{sc.PERSONALITY}'.")
            print(f"{INFO_HEADER} using '{file_parser_class.__name__}' file parser.")

            # Decide the bot class to use
            bot_class = FetchBot
            if url_param.get('start') is not None and url_param.get('end') is not None:
                bot_class = DateFetchBot
            print(f"{INFO_HEADER} using '{bot_class.__name__}' bot.")

        # *****************************************************************
        else:
            raise SystemExit(f"{EXCEPTION_HEADER} personality='{sc.PERSONALITY}' is invalid for fetch bot.")

        ############################# RUN THE BOT ###########################

        fetch_bot = bot_class(dbconn=dbconn)

        fetch_bot.run(api_address=api_address,
                      url_param=url_param,
                      select_apiparam_query=select_apiparam_query)



        end_time = time.perf_counter()
        print(20 * '-' + " PROGRAMS END SUCCESSFULLY " + 20 * '-')
        print(f"{INFO_HEADER} elapsed time: {end_time - start_time}")

    except SystemExit as ex:
        print(str(ex))
        sys.exit(1)
