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

# IMPORT MODULES
import airquality.core.logger.log as log
import airquality.bot.date_fetch_bot as dfb
import airquality.bot.fetch_bot as fb
import airquality.io.local.io as io
import airquality.io.remote.database.adapter as db
import airquality.utility.picker.query as pk
import airquality.utility.parser.file as fp
import airquality.data.builder.timest as ts
import airquality.data.builder.url as url
import airquality.data.reshaper.packet as rshp
import airquality.data.reshaper.uniform.api2db as a2d
import airquality.data.reshaper.uniform.db2api as d2a

# IMPORT CONSTANTS
import airquality.core.constants.system_constants as sc
from airquality.core.constants.shared_constants import QUERY_FILE, API_FILE, SERVER_FILE, VALID_PERSONALITIES, \
    FETCH_USAGE


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


################################ DEBUGGER AND LOGGER VARIABLES ################################
debugger = log.get_logger(use_color=True)
logger = log.get_logger(log_filename="fetch", log_sub_dir="log")


################################ MAIN FUNCTION ################################
def main():
    args = sys.argv[1:]
    if not args:
        debugger.warning(FETCH_USAGE)
        sys.exit(1)

    parse_sys_argv(args)

    try:
        start_time = time.perf_counter()
        ################################ READ SERVER FILE ################################
        raw_server_data = io.IOManager.open_read_close_file(path=SERVER_FILE)
        parser = fp.FileParserFactory.make_parser(file_extension=SERVER_FILE.split('.')[-1])
        parsed_server_data = parser.parse(text=raw_server_data)
        server_settings = parsed_server_data[sc.PERSONALITY]

        ################################ DATABASE CONNECTION ADAPTER ################################
        dbconn = db.Psycopg2DatabaseAdapter(server_settings)
        dbconn.open_conn()

        ################################ READ QUERY FILE ###############################
        raw_query_data = io.IOManager.open_read_close_file(path=QUERY_FILE)
        parser = fp.FileParserFactory.make_parser(file_extension=QUERY_FILE.split('.')[-1])
        parsed_query_data = parser.parse(text=raw_query_data)

        ################################ CREATE QUERY PICKER ###############################
        query_picker = pk.QueryPicker(parsed_query_data)

        ################################ READ API FILE ################################
        raw_api_data = io.IOManager.open_read_close_file(path=API_FILE)
        parser = fp.FileParserFactory.make_parser(file_extension=API_FILE.split('.')[-1])
        parsed_api_data = parser.parse(text=raw_api_data)

        ################################ GET THE API ADDRESS ################################
        try:
            api_address = parsed_api_data[sc.PERSONALITY]['api_address']
            url_param = parsed_api_data[sc.PERSONALITY]['url_param']
        except KeyError as ke:
            raise SystemExit(f"bad 'api.json' file structure => missing key={ke!s} for personality='{sc.PERSONALITY}'.")

        ################################ DATABASE SENSOR ID ASSOCIATED TO PERSONALITY ################################
        query = query_picker.select_sensor_ids_from_personality(personality=sc.PERSONALITY)
        answer = dbconn.send(query=query)
        sensor_ids = [t[0] for t in answer]

        if not sensor_ids:
            debugger.warning(f"no sensor found for personality='{sc.PERSONALITY}' => done")
            logger.warning(f"no sensor found for personality='{sc.PERSONALITY}' => done")
            dbconn.close_conn()
            return

        ################################ SELECT MEASURE PARAM FROM PERSONALITY ################################
        query = query_picker.select_measure_param_from_personality(personality=sc.PERSONALITY)
        answer = dbconn.send(query=query)
        measure_param_map = dict(answer)

        if not measure_param_map:
            debugger.warning(f"no measure param found for personality='{sc.PERSONALITY}' => done")
            logger.info(f"no measure param found for personality='{sc.PERSONALITY}' => done")
            dbconn.close_conn()
            return

        ################################ CHECK IF FORMAT EXISTS ################################

        bot_class = fb.FetchBot
        ############################# CREATE THE PROPER BOT OBJECT ###########################
        if sc.PERSONALITY == 'atmotube':
            if url_param.get('format') is None:
                raise SystemExit("bad 'api.json' file structure => missing 'format' key.")
            if url_param.get('date'):
                bot_class = dfb.DateFetchBot
            file_parser = fp.FileParserFactory().make_parser(url_param['format'])
            packet_reshaper = rshp.AtmotubePacketReshaper()
            api2db_reshaper = a2d.AtmotubeUniformReshaper()
            db2api_reshaper = d2a.AtmotubeUniformReshaper()
            url_builder_class = url.AtmotubeURLBuilder
            timest_fmt = ts.ATMOTUBE_FMT
        # *****************************************************************
        elif sc.PERSONALITY == 'thingspeak':
            if url_param.get('format') is None:
                raise SystemExit("bad 'api.json' file structure => missing 'format' key.")
            if url_param.get('start') or url_param.get('end'):
                bot_class = dfb.DateFetchBot
            file_parser = fp.FileParserFactory().make_parser(url_param['format'])
            packet_reshaper = rshp.ThingspeakPacketReshaper()
            api2db_reshaper = a2d.ThingspeakUniformReshaper()
            db2api_reshaper = d2a.ThingspeakUniformReshaper()
            url_builder_class = url.ThingspeakURLBuilder
            timest_fmt = ts.THINGSPK_FMT
        else:
            raise SystemExit(f"bad personality => fetch bot is not implemented for personality='{sc.PERSONALITY}'")

        ############################# BOT SETTINGS ###########################
        bot_settings_msg = f"personality={sc.PERSONALITY}, " \
                           f"debug={sc.DEBUG_MODE}, " \
                           f"file_parser={file_parser.__class__.__name__}," \
                           f" bot_class={bot_class.__name__}"
        debugger.info(bot_settings_msg)
        logger.info(bot_settings_msg)

        ############################# BUILD THE BOT ###########################
        fetch_bot = bot_class(dbconn=dbconn,
                              timest_fmt=timest_fmt,
                              file_parser=file_parser,
                              query_picker=query_picker,
                              packet_reshaper=packet_reshaper,
                              api2db_reshaper=api2db_reshaper,
                              db2api_reshaper=db2api_reshaper,
                              url_builder_class=url_builder_class)

        ############################# RUN THE BOT ###########################
        fetch_bot.run(api_address=api_address, opt_url_param=url_param, sensor_ids=sensor_ids)

        end_time = time.perf_counter()
        debugger.info(f"program successfully complete in {(end_time - start_time):0.04} seconds")
        logger.info(f"program successfully complete in {(end_time - start_time):0.04} seconds")

    except SystemExit as ex:
        debugger.error(str(ex))
        logger.error(str(ex))
        sys.exit(1)
