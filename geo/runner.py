#################################################
#
# @Author: davidecolombo
# @Date: gio, 28-10-2021, 11:13
# @Description: this script defines the main function for the geolocation bot that pulls the locations from the sensor
#               API and checks if there any updates to do.
#
#################################################
import sys
import time
from typing import List
import airquality.constants.system_constants as sc

# IMPORT CLASSES FROM AIRQUALITY MODULE
from airquality.io.io import IOManager
from airquality.bot.geo_bot import GeoBot
from airquality.picker.query_picker import QueryPicker
from airquality.geom.postgis_geometry import PostGISPoint
from airquality.api.url_builder import URLBuilderPurpleair
from airquality.parser.db_answer_parser import DatabaseAnswerParser
from airquality.reshaper.packet_reshaper import PurpleairPacketReshaper
from airquality.database.database_adapter import Psycopg2DatabaseAdapter
from airquality.parser.file_parser import FileParserFactory, JSONFileParser
from airquality.adapter.universal_db_adapter import PurpleairUniversalDatabaseAdapter
from airquality.container.sql_container import GeoSQLContainer, SQLContainerComposition

# IMPORT SHARED CONSTANTS
from airquality.constants.shared_constants import QUERY_FILE, API_FILE, SERVER_FILE, \
    DEBUG_HEADER, INFO_HEADER, EXCEPTION_HEADER, \
    GEO_USAGE, VALID_PERSONALITIES


################################ SYSTEM ARGS PARSER FUNCTION ################################
def parse_sys_argv(args: List[str]):
    if args[0] in ("--help", "-h"):
        print(GEO_USAGE)
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
        raise SystemExit(f"{parse_sys_argv.__name__}(): missing personality argument. \n{GEO_USAGE}")


################################ MAIN FUNCTION ################################
def main():
    args = sys.argv[1:]
    if not args:
        raise SystemExit(f"{main.__name__}: missing required arguments.\n {GEO_USAGE}")

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
        server_settings = parsed_server_data[sc.PERSONALITY]

        ################################ DATABASE CONNECTION ADAPTER ################################
        dbconn = Psycopg2DatabaseAdapter(server_settings)
        dbconn.open_conn()

        ################################ READ QUERY FILE ###############################
        raw_query_data = IOManager.open_read_close_file(path=QUERY_FILE)
        parser = FileParserFactory.file_parser_from_file_extension(file_extension=QUERY_FILE.split('.')[-1])
        parsed_query_data = parser.parse(raw_string=raw_query_data)

        ################################ CREATE QUERY PICKER ###############################
        query_picker = QueryPicker(parsed_query_data)

        ########################## QUERY THE ACTIVE LOCATION FOR PURPLEAIR SENSORS ################################
        query = query_picker.select_sensor_valid_name_geom_mapping_from_personality(personality=sc.PERSONALITY)
        answer = dbconn.send(executable_sql_query=query)
        active_locations = DatabaseAnswerParser.parse_key_val_answer(answer)

        if not active_locations:
            print(f"{INFO_HEADER} no sensor found for personality='{sc.PERSONALITY}'.")
            dbconn.close_conn()
            return

        if sc.DEBUG_MODE:
            print(20 * "=" + " SENSORS FOUND INTO THE DATABASE " + 20 * '=')
            for key, val in active_locations.items():
                print(f"{DEBUG_HEADER} {key}={val}")

        ####################### QUERY THE (SENSOR_NAME, SENSOR_ID) MAPPING FROM PERSONALITY ############################
        query = query_picker.select_sensor_name_id_mapping_from_personality(personality=sc.PERSONALITY)
        answer = dbconn.send(executable_sql_query=query)
        name2id_map = DatabaseAnswerParser.parse_key_val_answer(answer)

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

        ################################ GET THE NEEDED QUERY STATEMENT ################################
        update_valid_to_timestamp = query_picker.update_valid_to_timestamp_location()
        insert_into_sensor_at_location = query_picker.insert_into_sensor_at_location()

        if sc.PERSONALITY == 'purpleair':
            geo_bot = GeoBot(dbconn=dbconn,
                             url_builder_class=URLBuilderPurpleair,
                             file_parser_class=JSONFileParser,
                             reshaper_class=PurpleairPacketReshaper,
                             universal_db_adapter_class=PurpleairUniversalDatabaseAdapter,
                             geom_sqlcontainer_class=GeoSQLContainer,
                             composition_class=SQLContainerComposition,
                             postgis_geom_class=PostGISPoint)
        else:
            raise SystemExit(f"{EXCEPTION_HEADER} personality='{sc.PERSONALITY}' is invalid for geo bot.")

        ################################ RUN THE BOT ################################
        geo_bot.run(api_address=api_address,
                    url_param=url_param,
                    active_locations=active_locations,
                    name2id_map=name2id_map,
                    update_valid_to_ts_query=update_valid_to_timestamp,
                    sensor_at_location_query=insert_into_sensor_at_location)

        print(20 * '-' + " PROGRAMS END SUCCESSFULLY " + 20 * '-')
        end_time = time.perf_counter()
        print(f"{INFO_HEADER} total time = {end_time - start_time}")

    except Exception as ex:
        print(str(ex))
        if isinstance(ex, SystemExit):
            sys.exit(1)
