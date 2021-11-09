#################################################
#
# @Author: davidecolombo
# @Date: dom, 24-10-2021, 20:36
# @Description: this script defines the main function for the 'initialize' module

#               This module is used for loading for the first time the sensor's data to the
#
#################################################
import sys
import time
from typing import List
import airquality.constants.system_constants as sc
from airquality.bot.initialize_bot import InitializeBot

# IMPORT CLASSES FROM AIRQUALITY MODULE
from airquality.io.io import IOManager
from airquality.picker.query_picker import QueryPicker
from airquality.geom.postgis_geometry import PostGISPoint
from airquality.api.url_builder import URLBuilderPurpleair
from airquality.picker.resource_picker import ResourcePicker
from airquality.parser.db_answer_parser import DatabaseAnswerParser
from airquality.reshaper.packet_reshaper import PurpleairPacketReshaper
from airquality.adapter.universal_db_adapter import PurpleairUniversalDatabaseAdapter
from airquality.parser.file_parser import JSONFileParser, FileParserFactory
from airquality.database.db_conn_adapter import Psycopg2ConnectionAdapterFactory
from airquality.container.sql_container import SQLContainerComposition, SensorSQLContainer, \
    APIParamSQLContainer, GeoSQLContainer

# IMPORT SHARED CONSTANTS
from airquality.constants.shared_constants import QUERY_FILE, API_FILE, SERVER_FILE, \
    DEBUG_HEADER, INFO_HEADER, EXCEPTION_HEADER, \
    VALID_PERSONALITIES, INITIALIZE_USAGE


################################ SYSTEM ARGS PARSER FUNCTION ################################
def parse_sys_argv(args: List[str]):
    if args[0] in ("--help", "-h"):
        print(INITIALIZE_USAGE)
        sys.exit(0)

    is_personality_set = False

    for arg in args:
        if arg in ("-d", "--debug"):
            sc.DEBUG_MODE = True
        elif arg in VALID_PERSONALITIES and not is_personality_set:
            sc.PERSONALITY = arg
            is_personality_set = True
        else:
            print(f"{parse_sys_argv.__name__}(): ignoring invalid option '{arg}'")

    if not is_personality_set:
        raise SystemExit(f"{parse_sys_argv.__name__}(): missing personality argument. \n{INITIALIZE_USAGE}")


################################ MAIN FUNCTION ################################
def main():
    args = sys.argv[1:]
    if not args:
        raise SystemExit(f"{main.__name__}: missing required arguments. {INITIALIZE_USAGE}")

    parse_sys_argv(args)
    print(f"{INFO_HEADER} personality = {sc.PERSONALITY}")
    print(f"{INFO_HEADER} debug       = {sc.DEBUG_MODE}")

    try:
        start_time = time.perf_counter()
        print(20 * '-' + " START THE PROGRAM " + 20 * '-')

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

        ################################ SELECT SENSOR NAME FROM DATABASE ################################
        query = query_picker.select_sensor_name_from_personality(personality=sc.PERSONALITY)
        answer = dbconn.send(executable_sql_query=query)
        sensor_names = DatabaseAnswerParser.parse_single_attribute_answer(response=answer)

        if not sensor_names:
            print(f"{INFO_HEADER} no sensor found into the database for personality='{sc.PERSONALITY}'.")
        else:
            if sc.DEBUG_MODE:
                print(20 * "=" + " SENSORS FOUND INTO THE DATABASE " + 20 * '=')
                for name in sensor_names:
                    print(f"{DEBUG_HEADER} name='{name}'.")

        ####################### SELECT THE MAX SENSOR ID PRESENT INTO THE DATABASE ########################
        query = query_picker.select_max_sensor_id()
        answer = dbconn.send(executable_sql_query=query)
        max_sensor_id = DatabaseAnswerParser.parse_single_attribute_answer(answer)

        ####################### DEFINE THE FIRST SENSOR ID FROM WHERE TO START ########################
        first_sensor_id = 1
        if max_sensor_id[0] is not None:
            print(f"{INFO_HEADER} max sensor_id found in the database is => {str(max_sensor_id[0])}.")
            first_sensor_id = max_sensor_id[0] + 1

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

        ################################ GET QUERY STATEMENT FOR INSERTION ################################
        insert_into_sensor_statement = query_picker.insert_into_sensor()
        insert_into_api_param_statement = query_picker.insert_into_api_param()
        insert_into_sensor_at_location_statement = query_picker.insert_into_sensor_at_location()

        ###################### INSTANTIATE THE BOT WITH THE PROPER CLASSES BASED ON PERSONALITY ########################
        if sc.PERSONALITY == 'purpleair':
            initialize_bot = InitializeBot(dbconn=dbconn,
                                           file_parser_class=JSONFileParser,
                                           url_builder_class=URLBuilderPurpleair,
                                           reshaper_class=PurpleairPacketReshaper,
                                           universal_adapter_class=PurpleairUniversalDatabaseAdapter,
                                           geo_sqlcontainer_class=GeoSQLContainer,
                                           sensor_sqlcontainer_class=SensorSQLContainer,
                                           apiparam_sqlcontainer_class=APIParamSQLContainer,
                                           composition_class=SQLContainerComposition,
                                           postgis_geom_class=PostGISPoint)
        else:
            raise SystemExit(f"{EXCEPTION_HEADER} personality='{sc.PERSONALITY}' is invalid for initialize bot.")

        ################################ RUN THE BOT ################################
        initialize_bot.run(first_sensor_id=first_sensor_id,
                           api_address=api_address,
                           url_param=url_param,
                           sensor_names=sensor_names,
                           sensor_query=insert_into_sensor_statement,
                           api_param_query=insert_into_api_param_statement,
                           sensor_at_location_query=insert_into_sensor_at_location_statement)

        print(20 * '-' + " PROGRAMS END SUCCESSFULLY " + 20 * '-')
        end_time = time.perf_counter()
        print(f"{INFO_HEADER} total time = {end_time - start_time}")

    except Exception as ex:
        print(str(ex))
        if isinstance(ex, SystemExit):
            sys.exit(1)
