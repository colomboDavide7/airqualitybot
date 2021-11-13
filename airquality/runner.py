######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 11/11/21 12:48
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import os
import sys
import dotenv

# IMPORT MODULES
import airquality.core.logger.log as log
import airquality.core.logger.fmt as formt
import airquality.stream.local.structured.json as struct
import airquality.stream.remote.database.adapter as db
import airquality.data.builder.timest as ts
import airquality.data.builder.url as url
import airquality.data.builder.geom as geom
import airquality.utility.picker.query as pk
import airquality.utility.parser.text as txt
import airquality.data.extractor.api as ext
import airquality.data.reshaper.uniform.sensor as sens
import airquality.data.reshaper.uniform.param as par
import airquality.data.reshaper.uniform.measure as meas
import airquality.bot.fact as fact

################################ GLOBAL VARIABLES ################################
USAGE = "USAGE: python(version) -m airquality bot_name sensor_type"
API_FILE = "properties/api.json"
QUERY_FILE = "properties/query.json"


################################ ENTRY POINT OF THE PROGRAM ################################
def main():

    handler_cls = log.get_handler_cls(use_file=True)
    handler = handler_cls('log/errors.log', 'a+')
    fmt_cls = formt.get_formatter_cls()
    fmt = fmt_cls(formt.FMT_STR)
    error_logger = log.get_logger(handler=handler, formatter=fmt)

    args = sys.argv[1:]
    if not args:
        error_logger.error(f"'{main.__name__}()': bad usage => missing required arguments")
        print(f"{USAGE}")
        sys.exit(1)

    settings_string = ""
    # Extract arguments
    bot_name = args[0]
    sensor_type = args[1]

    # Create 'logger'
    handler_cls = log.get_handler_cls(use_file=True)
    handler = handler_cls(f'log/{bot_name}.log', 'a+')
    fmt_cls = formt.get_formatter_cls()
    fmt = fmt_cls(formt.FMT_STR)
    logger = log.get_logger(handler=handler, formatter=fmt)

    # Create 'debugger'
    handler_cls = log.get_handler_cls(use_file=False)
    handler = handler_cls()
    fmt_cls = formt.get_formatter_cls(use_color=True)
    fmt = fmt_cls(formt.FMT_STR)
    debugger = log.get_logger(handler=handler, formatter=fmt)

    try:

        # Get the 'bot_class' to use in the program
        bot_class = fact.get_bot_class(bot_name=bot_name, sensor_type=sensor_type)
        settings_string += f"success => bot_class={bot_class.__name__}, sensor_type={sensor_type}, "

        # Load '.env' file
        dotenv.load_dotenv(dotenv_path="./properties/.env")

        # Open database connection
        if not os.environ.get('DBCONN'):
            raise SystemExit(f"'{main.__name__}()': bad '.env' file structure => missing param='DBCONN'")
        dbconn = db.Psycopg2DatabaseAdapter(os.environ['DBCONN'])

        # Query file object
        query_file = struct.JSONFile(QUERY_FILE)
        query_picker = pk.QueryPicker(query_file)

        # API file object
        api_file = struct.JSONFile(API_FILE, path_to_object=[sensor_type])
        address = api_file.api_address
        url_param = api_file.url_param

        # Append secret 'api_key' for purpleair sensors
        if sensor_type == 'purpleair':
            if not os.environ.get('PURPLEAIR_API_KEY'):
                raise SystemExit(f"'{main.__name__}()': bad '.env' file structure => missing param='PURPLEAIR_API_KEY'")
            url_param['api_key'] = os.environ['PURPLEAIR_API_KEY']

        # TextParser class
        if sensor_type == 'purpleair':
            text_parser_class = txt.JSONParser
        else:
            if not url_param.get('format'):
                raise SystemExit(f"'{main.__name__}()': bad 'api.json' file structure => missing param='format'")
            text_parser_class = txt.get_parser_class(url_param['format'])

        # Update settings string
        settings_string += f"text_parser_class={text_parser_class.__name__}, "

        # URLBuilder class
        url_class = url.get_url_class(sensor_type)
        url_builder = url_class(address=address, url_param=url_param)
        settings_string += f"url_class={url_class.__name__}, "

        # APIExtractor class
        extractor_class = ext.get_api_extractor_class(sensor_type)
        settings_string += f"extractor_class={extractor_class.__name__}, "

        # Create the bot instance
        bot = bot_class(sensor_type=sensor_type, dbconn=dbconn)

        # Add external dependencies
        bot.add_url_builder(url_builder)
        bot.add_api_extractor_class(extractor_class)
        bot.add_query_picker(query_picker)
        bot.add_text_parser_class(text_parser_class)

        if bot_name in ('init', 'update'):
            sensor_rshp_class = sens.get_sensor_reshaper_class(sensor_type)
            bot.add_sensor_rshp_class(sensor_rshp_class)
            settings_string += f"sensor_rshp_class={sensor_rshp_class.__name__}, "
            bot.add_geom_builder_class(geom.PointBuilder)
            settings_string += f"geom_builder_class={geom.PointBuilder.__name__}, "
            bot.add_current_ts(ts.CurrentTimestamp())

        # ParamReshaper class
        if bot_name == 'fetch':
            param_rshp_class = par.get_param_reshaper_class(sensor_type)
            bot.add_param_rshp_class(param_rshp_class)
            settings_string += f"param_rshp_class={param_rshp_class.__name__}, "

        if bot_name == 'fetch':
            # MeasureReshaper class
            measure_rshp_class = meas.get_measure_reshaper_class(sensor_type)
            bot.add_measure_rshp_class(measure_rshp_class)
            settings_string += f"measure_rshp_class={measure_rshp_class.__name__}, "

        # Add timestamp format dependency
        if bot_name == 'fetch':
            fmt = ts.get_timest_fmt(sensor_type)
            bot.set_timest_fmt(fmt)
            settings_string += f"timest_fmt={fmt}, "

        # Debug and log the program settings
        settings_string = settings_string.strip(', ')
        debugger.info(settings_string)
        logger.info(settings_string)

        # Add debugger and logger to bot
        bot.add_debugger(debugger)
        bot.add_logger(logger)
        bot.log_filename = bot_name
        bot.log_sub_dir = 'log'

        # Run the bot
        bot.run()

        # Close database connection
        dbconn.close_conn()
        debugger.info("success => database connection closed")
        logger.info("success => database connection closed")

    ################################ HANDLE EXCEPTIONS ################################
    except (SystemExit, AttributeError, KeyError) as ex:
        debugger.error(f"{ex!s}")
        error_logger.error(f"{ex!s}")
        sys.exit(1)
