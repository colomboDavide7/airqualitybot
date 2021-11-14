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
import airquality.logger.log as log
import airquality.logger.fmt as formt
import airquality.bot.util.fact as fact
import airquality.file.structured.json as struct
import airquality.file.util.parser as txt
import airquality.database.conn as db
import airquality.database.util.datatype.timestamp as ts
import airquality.database.util.postgis.geom as geom
import airquality.database.util.sql.query as pk
import airquality.api.util.extractor as ext
import airquality.api.util.url as url
import airquality.adapter.api2db.sensor as sens
import airquality.adapter.db2api.param as par
import airquality.adapter.api2db.measure as meas
import airquality.adapter.file2db.param as fadapt
import airquality.bot.util.executor as exc
import airquality.bot.util.datelooper as loop
import airquality.bot.util.filter as filt


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
        query_builder = pk.QueryBuilder(query_file)

        # API file object
        api_file = struct.JSONFile(API_FILE, path_to_object=[sensor_type])
        address = api_file.api_address
        url_param = api_file.url_param

        # Append secret 'api_key' for purpleair sensors
        if sensor_type == 'purpleair':
            file_adapt_class = fadapt.get_file_adapter_class(sensor_type)
            env_param = file_adapt_class().adapt()
            url_param.update(env_param)

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
        bot = bot_class()

        # Add external dependencies
        bot.add_url_builder(url_builder)
        bot.add_api_extractor_class(extractor_class)
        bot.add_text_parser_class(text_parser_class)

        # Define timest_class
        timest_cls = ts.get_timest_class(sensor_type)
        settings_string += f"timest_cls={timest_cls.__name__}, "

        # Add DateFilter dependency
        if bot_name == 'fetch':
            date_filter = filt.DateFilter(timest_cls=timest_cls)
            date_filter.set_debugger(debugger)
            date_filter.set_logger(logger)
            bot.add_packet_filter(date_filter)
            settings_string += f"packet_filter_class={date_filter.__class__.__name__}, "
        elif bot_name == 'init':
            name_filter = filt.NameFilter()
            name_filter.set_logger(logger)
            name_filter.set_debugger(debugger)
            bot.add_packet_filter(name_filter)
            settings_string += f"packet_filter_class={name_filter.__class__.__name__}, "

        # Add timestamp format + PacketQueryExecutor dependencies
        if bot_name in ('init', 'update'):
            packet_executor = exc.PacketQueryExecutor(query_builder=query_builder, conn=dbconn,
                                                      timest_cls=timest_cls, geom_builder_cls=geom.PointBuilder)
            packet_executor.set_debugger(debugger)
            packet_executor.set_logger(logger)
            bot.add_packet_query_executor(packet_executor)
            settings_string += f"packet_query_executor_class={packet_executor.__class__.__name__}, "

        if bot_name in ('init', 'update'):
            sensor_rshp_class = sens.get_sensor_adapter_class(sensor_type)
            bot.add_sensor_rshp_class(sensor_rshp_class)
            settings_string += f"sensor_rshp_class={sensor_rshp_class.__name__}, "

        # ParamReshaper class
        if bot_name == 'fetch':
            param_rshp_class = par.get_param_adapter_class(sensor_type)
            bot.add_param_rshp_class(param_rshp_class)
            settings_string += f"param_rshp_class={param_rshp_class.__name__}, "

        if bot_name == 'fetch':
            # MeasureReshaper class
            measure_rshp_class = meas.get_measure_adapter_class(sensor_type)
            bot.add_measure_rshp_class(measure_rshp_class)
            settings_string += f"measure_rshp_class={measure_rshp_class.__name__}, "

        # Add DateLooper dependency
        if bot_name == 'fetch':
            date_looper_cls = loop.get_date_looper_class(sensor_type)
            bot.add_date_looper_class(date_looper_cls)
            settings_string += f"date_looper_class={date_looper_cls.__name__}, "

        # Add SensorQueryExecutor dependency
        if bot_name == 'fetch':
            sensor_query_executor = exc.SensorQueryExecutor(conn=dbconn, query_builder=query_builder)
            bot.add_sensor_query_executor(sensor_query_executor)
            settings_string += f"sensor_query_executor={sensor_query_executor.__class__.__name__}, "

        # Add BotQueryExecutor dependency
        if bot_name in ('fetch', 'init', 'update'):
            bot_query_executor = exc.BotQueryExecutor(conn=dbconn, query_builder=query_builder, sensor_type=sensor_type)
            bot_query_executor.set_logger(logger)
            bot_query_executor.set_debugger(debugger)
            bot.add_bot_query_executor(bot_query_executor)
            settings_string += f"bot_query_executor={bot_query_executor.__class__.__name__}, "

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
