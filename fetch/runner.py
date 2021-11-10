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
from airquality.core.constants.shared_constants import QUERY_FILE, API_FILE, SERVER_FILE, \
    DEBUG_HEADER, INFO_HEADER, EXCEPTION_HEADER, \
    VALID_PERSONALITIES, FETCH_USAGE


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
            raise SystemExit(f"{EXCEPTION_HEADER} bad 'api.json' file structure => missing key={ke!s} "
                             f"for personality='{sc.PERSONALITY}'.")

        ################################ DATABASE SENSOR ID ASSOCIATED TO PERSONALITY ################################
        query = query_picker.select_sensor_ids_from_personality(personality=sc.PERSONALITY)
        answer = dbconn.send(query=query)
        sensor_ids = [t[0] for t in answer]

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
        answer = dbconn.send(query=query)
        measure_param_map = dict(answer)
        if sc.DEBUG_MODE:
            print(20 * "=" + " MEASURE PARAM MAPPING " + 20 * '=')
            for param_code, param_id in measure_param_map.items():
                print(f"{DEBUG_HEADER} {param_code}={param_id}")

        ################################ CHECK IF FORMAT EXISTS ################################

        bot_class = fb.FetchBot
        ############################# CREATE THE PROPER BOT OBJECT ###########################
        if sc.PERSONALITY == 'atmotube':
            if url_param.get('format') is None:
                raise SystemExit(f"{EXCEPTION_HEADER} bad 'api.json' file structure => missing 'format' key.")
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
                raise SystemExit(f"{EXCEPTION_HEADER} bad 'api.json' file structure => missing 'format' key.")
            if url_param.get('start') or url_param.get('end'):
                bot_class = dfb.DateFetchBot
            file_parser = fp.FileParserFactory().make_parser(url_param['format'])
            packet_reshaper = rshp.ThingspeakPacketReshaper()
            api2db_reshaper = a2d.ThingspeakUniformReshaper()
            db2api_reshaper = d2a.ThingspeakUniformReshaper()
            url_builder_class = url.ThingspeakURLBuilder
            timest_fmt = ts.THINGSPK_FMT
        else:
            raise SystemExit(
                f"{EXCEPTION_HEADER} bad personality => fetch bot is not implemented for personality='{sc.PERSONALITY}'.")

        ############################# BOT SETTINGS ###########################
        print(f"{INFO_HEADER} using '{file_parser.__class__.__name__}' file parser.")
        print(f"{INFO_HEADER} using '{bot_class.__name__}' bot.")

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
        fetch_bot.run(api_address=api_address, url_param=url_param, sensor_ids=sensor_ids)

        end_time = time.perf_counter()
        print(20 * '-' + " PROGRAMS END SUCCESSFULLY " + 20 * '-')
        print(f"{INFO_HEADER} elapsed time: {end_time - start_time}")

    except SystemExit as ex:
        print(str(ex))
        sys.exit(1)
