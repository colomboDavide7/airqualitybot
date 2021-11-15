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
import airquality.bot.util.executor.insert as ins
import airquality.bot.util.executor.select as sel
import airquality.bot.util.datelooper as loop
import airquality.bot.util.filter as filt

################################ GLOBAL VARIABLES ################################
USAGE = "USAGE: python(version) -m airquality bot_name sensor_type"
API_FILE = "properties/api.json"
QUERY_FILE = "properties/query.json"


def make_console_debugger(use_color=True):
    """Function that creates a Logger with a StreamHandler and a ColoredFormatter"""

    handler_cls = log.get_handler_cls(use_file=False)
    handler = handler_cls()
    fmt_cls = formt.get_formatter_cls(use_color)
    fmt = fmt_cls(formt.FMT_STR)
    return log.get_logger(handler=handler, formatter=fmt)


def make_file_logger(file_path: str, mode='a+'):
    """Function that creates a Logger instance with a FileHandler and a CustomFormatter"""

    handler_cls = log.get_handler_cls(use_file=True)
    handler = handler_cls(file_path, mode)
    fmt_cls = formt.get_formatter_cls()
    fmt = fmt_cls(formt.FMT_STR)
    return log.get_logger(handler=handler, formatter=fmt)


################################ ENTRY POINT OF THE PROGRAM ################################
def main():

    # Create an 'error_logger' that keep trace only of errors
    error_logger = make_file_logger(file_path='log/errors.log')

    # Argument checking
    args = sys.argv[1:]
    if not args:
        error_logger.error(f"'{main.__name__}()': bad usage => missing required arguments")
        print(USAGE)
        sys.exit(1)

    bot_name = args[0]              # 'bot name' identifies the broader operation of the bot
    sensor_type = args[1]           # 'sensor_type' identifies how the operations are specifically handled

    logger = make_file_logger(file_path=f'log/{bot_name}.log')              # Create specific file 'logger'
    debugger = make_console_debugger(use_color=True)                        # Create console 'debugger'

    messages = []                   # define a list of messages to log both on file and console

    try:
        # Get the 'bot_class' to use in the program
        bot_class = fact.get_bot_class(bot_name=bot_name, sensor_type=sensor_type)
        messages.append(f"bot_class={bot_class.__name__}")
        messages.append(f"sensor_type={sensor_type}")

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
        messages.append(f"text_parser_class={text_parser_class.__name__}")

        # URLBuilder class
        url_class = url.get_url_class(sensor_type)
        url_builder = url_class(address=address, url_param=url_param)
        messages.append(f"url_class={url_class.__name__}")

        # APIExtractor class
        extractor_class = ext.get_api_extractor_class(sensor_type)
        messages.append(f"extractor_class={extractor_class.__name__}")

        # Create the bot instance
        bot = bot_class()

        # Add external dependencies
        bot.add_url_builder(url_builder)
        bot.add_api_extractor_class(extractor_class)
        bot.add_text_parser_class(text_parser_class)

        # Define timest_class
        timest_cls = ts.get_timest_class(sensor_type)
        messages.append(f"timest_cls={timest_cls.__name__}")

        # Add DateFilter dependency
        if bot_name == 'fetch':
            date_filter = filt.DateFilter(timest_cls=timest_cls)
            date_filter.set_debugger(debugger)
            date_filter.set_logger(logger)
            bot.add_packet_filter(date_filter)
            messages.append(f"packet_filter_class={date_filter.__class__.__name__}")
        elif bot_name == 'init':
            name_filter = filt.NameFilter()
            name_filter.set_logger(logger)
            name_filter.set_debugger(debugger)
            bot.add_packet_filter(name_filter)
            messages.append(f"packet_filter_class={name_filter.__class__.__name__}")

        # Get InsertionQueryExecutor class
        insertion_executor_class = ins.get_insertion_executor_class(sensor_type)
        insertion_executor = insertion_executor_class(query_builder=query_builder, conn=dbconn, timest_cls=timest_cls)
        insertion_executor.set_debugger(debugger)
        insertion_executor.set_logger(logger)

        # Add PostGIS geometry dependency
        if sensor_type == 'purpleair':
            insertion_executor.set_postgis_class(geom.PointBuilder)

        # Add InsertionQueryExecutor dependency
        bot.add_insertion_executor(insertion_executor)
        messages.append(f"insertion_executor_class={insertion_executor_class.__name__}")

        if bot_name in ('init', 'update'):
            sensor_rshp_class = sens.get_sensor_adapter_class(sensor_type)
            bot.add_sensor_rshp_class(sensor_rshp_class)
            messages.append(f"sensor_reshaper_class={sensor_rshp_class.__name__}")

        # ParamReshaper class
        if bot_name == 'fetch':
            param_rshp_class = par.get_param_adapter_class(sensor_type)
            bot.add_param_rshp_class(param_rshp_class)
            messages.append(f"param_reshaper_class={param_rshp_class.__name__}")

        # MeasureReshaper class
        if bot_name == 'fetch':
            measure_rshp_class = meas.get_measure_adapter_class(sensor_type)
            bot.add_measure_rshp_class(measure_rshp_class)
            messages.append(f"measure_reshaper_class={measure_rshp_class.__name__}")

        # Add DateLooper dependency
        if bot_name == 'fetch':
            date_looper_cls = loop.get_date_looper_class(sensor_type)
            bot.add_date_looper_class(date_looper_cls)
            messages.append(f"date_looper_class={date_looper_cls.__name__}")

        # Add SensorQueryExecutor dependency
        if bot_name == 'fetch':
            sensor_query_executor = sel.SensorQueryExecutor(conn=dbconn, query_builder=query_builder)
            bot.add_sensor_query_executor(sensor_query_executor)
            messages.append(f"sensor_query_executor={sensor_query_executor.__class__.__name__}")

        # Add BotQueryExecutor dependency
        bot_query_executor = sel.BotQueryExecutor(conn=dbconn, query_builder=query_builder, sensor_type=sensor_type)
        bot_query_executor.set_logger(logger)
        bot_query_executor.set_debugger(debugger)
        bot.add_bot_query_executor(bot_query_executor)
        messages.append(f"bot_query_executor={bot_query_executor.__class__.__name__}")

        # Debug and log the program settings
        for msg in messages:
            debugger.debug(msg)
            logger.debug(msg)

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
