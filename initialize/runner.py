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

# IMPORT MODULES
import airquality.core.logger.log as log
import airquality.bot.init as bot
import airquality.io.local.io as io
import airquality.io.remote.database.adapter as db
import airquality.utility.picker.query as pk
import airquality.utility.parser.text as fp
import airquality.data.builder.timest as ts
import airquality.data.builder.geom as gb
import airquality.data.builder.url as url
import data.extractor.api as rshp
import airquality.data.reshaper.uniform.api2db as a2d

# IMPORT CONSTANTS
import airquality.core.constants.system_constants as sc
from airquality.core.constants.shared_constants import QUERY_FILE, API_FILE, SERVER_FILE, VALID_PERSONALITIES, INITIALIZE_USAGE


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


################################ DEBUGGER AND LOGGER VARIABLES ################################
debugger = log.get_logger(use_color=True)
logger = log.get_logger(log_filename="initialize", log_sub_dir="log")


################################ MAIN FUNCTION ################################
def main():
    args = sys.argv[1:]
    if not args:
        raise SystemExit(f"{main.__name__}: missing required arguments. {INITIALIZE_USAGE}")

    parse_sys_argv(args)

    try:
        start_time = time.perf_counter()
        ################################ READ SERVER FILE ################################
        raw_server_data = io.IOManager.open_read_close_file(path=SERVER_FILE)
        parser = fp.FileParserFactory.make_parser(file_ext=SERVER_FILE.split('.')[-1])
        parsed_server_data = parser.parse(text=raw_server_data)
        server_settings = parsed_server_data[sc.PERSONALITY]

        ################################ DATABASE CONNECTION ADAPTER ################################
        dbconn = db.Psycopg2DatabaseAdapter(server_settings)
        dbconn.open_conn()

        ################################ READ QUERY FILE ###############################
        raw_query_data = io.IOManager.open_read_close_file(path=QUERY_FILE)
        parser = fp.FileParserFactory.make_parser(file_ext=QUERY_FILE.split('.')[-1])
        parsed_query_data = parser.parse(text=raw_query_data)

        ################################ CREATE QUERY PICKER ###############################
        query_picker = pk.QueryPicker(parsed_query_data)

        ################################ SELECT SENSOR NAME FROM DATABASE ################################
        query = query_picker.select_sensor_names_from_sensor_type(sensor_type=sc.PERSONALITY)
        answer = dbconn.send(query=query)
        sensor_names = [t[0] for t in answer]

        if not sensor_names:
            debugger.info(f"no sensor found into the database for personality='{sc.PERSONALITY}'")
            logger.info(f"no sensor found into the database for personality='{sc.PERSONALITY}'")

        ####################### SELECT THE MAX SENSOR ID PRESENT INTO THE DATABASE ########################
        query = query_picker.select_max_sensor_id()
        answer = dbconn.send(query=query)
        max_sensor_id = [t[0] for t in answer]

        ####################### DEFINE THE FIRST SENSOR ID FROM WHERE TO START ########################
        first_sensor_id = 1
        if max_sensor_id[0] is not None:
            first_sensor_id = max_sensor_id[0] + 1
            msg = f"database max sensor_id found is: {max_sensor_id[0]!s} => new insertion starts at: {first_sensor_id!s}"
            debugger.info(msg)
            logger.info(msg)

        ################################ READ API FILE ################################
        raw_api_data = io.IOManager.open_read_close_file(path=API_FILE)
        parser = fp.FileParserFactory.make_parser(file_ext=API_FILE.split('.')[-1])
        parsed_api_data = parser.parse(text=raw_api_data)

        ################################ GET THE API ADDRESS ################################
        try:
            api_address = parsed_api_data[sc.PERSONALITY]['api_address']
            url_param = parsed_api_data[sc.PERSONALITY]['url_param']
        except KeyError as ke:
            raise SystemExit(f"bad 'api.json' file structure => missing key={ke!s}.")

        ################################ GET THE API ADDRESS ################################
        current_ts = ts.CurrentTimestamp()
        file_parser = fp.JSONParser()

        ###################### INSTANTIATE THE BOT WITH THE PROPER CLASSES BASED ON PERSONALITY ########################
        if sc.PERSONALITY == 'purpleair':
            url_builder = url.PurpleairURL(address=api_address, querystr_param=url_param)
            packet_reshaper = rshp.PurpleairAPIExtractor()
            api2db_uniform_reshaper = a2d.PurpleairUniformReshaper()
            initialize_bot = bot.InitializeBot(dbconn=dbconn,
                                               timestamp=current_ts,
                                               file_parser=file_parser,
                                               packet_reshaper=packet_reshaper,
                                               query_picker=query_picker,
                                               url_builder=url_builder,
                                               api2db_uniform_reshaper=api2db_uniform_reshaper,
                                               geom_builder_class=gb.PointBuilder)
        else:
            raise SystemExit(f"bad personality => init bot is not implemented for personality='{sc.PERSONALITY}'.")

        ############################# BOT SETTINGS ###########################
        bot_settings_msg = f"personality={sc.PERSONALITY}, " \
                           f"file_parser={file_parser.__class__.__name__}," \
                           f" bot_class={initialize_bot.__name__}"
        debugger.info(bot_settings_msg)
        logger.info(bot_settings_msg)

        ################################ RUN THE BOT ################################
        initialize_bot.run(first_sensor_id=first_sensor_id, database_sensor_names=sensor_names)

        end_time = time.perf_counter()
        debugger.info(f"program successfully complete in {(end_time - start_time):0.04} seconds")
        logger.info(f"program successfully complete in {(end_time - start_time):0.04} seconds")

    except SystemExit as ex:
        debugger.error(str(ex))
        logger.error(str(ex))
        sys.exit(1)
