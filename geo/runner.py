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

# IMPORT MODULES
import airquality.bot.geo_bot as bot
import airquality.io.local.io as io
import airquality.io.remote.database.adapter as db
import airquality.utility.picker.query as pk
import airquality.utility.parser.file as fp
import airquality.data.builder.timest as ts
import airquality.data.builder.geom as gb
import airquality.data.builder.url as url
import airquality.data.reshaper.packet as rshp
import airquality.data.reshaper.uniform.api2db as a2d

# IMPORT CONSTANTS
import airquality.core.constants.system_constants as sc
from airquality.core.constants.shared_constants import QUERY_FILE, API_FILE, SERVER_FILE, \
    DEBUG_HEADER, INFO_HEADER, EXCEPTION_HEADER, \
    VALID_PERSONALITIES, GEO_USAGE


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
        raw_server_data = io.IOManager.open_read_close_file(SERVER_FILE)
        parser = fp.FileParserFactory.make_parser(file_extension=SERVER_FILE.split('.')[-1])
        parsed_server_data = parser.parse(raw_server_data)
        server_settings = parsed_server_data[sc.PERSONALITY]

        ################################ DATABASE CONNECTION ADAPTER ################################
        dbconn = db.Psycopg2DatabaseAdapter(server_settings)
        dbconn.open_conn()

        ################################ READ QUERY FILE ###############################
        raw_query_data = io.IOManager.open_read_close_file(QUERY_FILE)
        parser = fp.FileParserFactory.make_parser(file_extension=QUERY_FILE.split('.')[-1])
        parsed_query_data = parser.parse(raw_query_data)

        ################################ CREATE QUERY PICKER ###############################
        query_picker = pk.QueryPicker(parsed_query_data)

        ########################## QUERY THE ACTIVE LOCATION FOR PURPLEAIR SENSORS ################################
        query = query_picker.select_active_sensor_location(sc.PERSONALITY)
        answer = dbconn.send(query)
        active_locations = dict(answer)

        if not active_locations:
            print(f"{INFO_HEADER} no sensor found for personality='{sc.PERSONALITY}'.")
            dbconn.close_conn()
            return

        if sc.DEBUG_MODE:
            print(20 * "=" + " SENSORS FOUND INTO THE DATABASE " + 20 * '=')
            for key, val in active_locations.items():
                print(f"{DEBUG_HEADER} {key}={val}")

        ####################### QUERY THE (SENSOR_NAME, SENSOR_ID) MAPPING FROM PERSONALITY ############################
        query = query_picker.select_sensor_name_id_mapping_from_personality(sc.PERSONALITY)
        answer = dbconn.send(query)
        name2id_map = dict(answer)

        ################################ READ API FILE ################################
        raw_api_data = io.IOManager.open_read_close_file(API_FILE)
        parser = fp.FileParserFactory.make_parser(file_extension=API_FILE.split('.')[-1])
        parsed_api_data = parser.parse(raw_api_data)

        ################################ GET THE API ADDRESS ################################
        try:
            api_address = parsed_api_data[sc.PERSONALITY]['api_address']
            url_param = parsed_api_data[sc.PERSONALITY]['url_param']
        except KeyError as ke:
            raise SystemExit(
                f"{EXCEPTION_HEADER} bad 'api.json' file structure => missing key={ke!s} for personality='{sc.PERSONALITY}'."
            )

        ################################ MAKE COMMON VARIABLES FOR ALL THE BOTS ################################
        current_ts = ts.CurrentTimestamp()
        file_parser = fp.JSONFileParser()

        if sc.PERSONALITY == 'purpleair':
            url_builder = url.PurpleairURLBuilder(api_address=api_address, parameters=url_param)
            packet_reshaper = rshp.PurpleairPacketReshaper()
            uniform_reshaper = a2d.PurpleairUniformReshaper()
            geo_bot = bot.GeoBot(dbconn=dbconn,
                                 current_ts=current_ts,
                                 file_parser=file_parser,
                                 query_picker=query_picker,
                                 url_builder=url_builder,
                                 packet_reshaper=packet_reshaper,
                                 api2db_uniform_reshaper=uniform_reshaper,
                                 geom_builder_class=gb.PointBuilder)
        else:
            raise SystemExit(
                f"{EXCEPTION_HEADER} bad personality => geo bot is not implemented for personality='{sc.PERSONALITY}'.")

        ################################ RUN THE BOT ################################
        geo_bot.run(active_locations=active_locations, name2id_map=name2id_map)

        print(20 * '-' + " PROGRAMS END SUCCESSFULLY " + 20 * '-')
        end_time = time.perf_counter()
        print(f"{INFO_HEADER} total time = {end_time - start_time}")

    except Exception as ex:
        print(str(ex))
        if isinstance(ex, SystemExit):
            sys.exit(1)
