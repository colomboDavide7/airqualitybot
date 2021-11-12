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
import airquality.io.local.structured.json as struct
import airquality.io.remote.database.adapter as db
import airquality.data.builder.timest as ts
import airquality.data.builder.url as url
import airquality.data.builder.geom as geom
import airquality.utility.picker.query as pk
import airquality.utility.parser.text as txt
import airquality.data.extractor.api as ext
import airquality.data.reshaper.uniform.api2db as a2d
import airquality.data.reshaper.uniform.db2api as d2a
import airquality.bot.fact as fact

################################ GLOBAL VARIABLES ################################
USAGE = "python(version) -m airquality bot_name sensor_type"
API_FILE = "properties/api.json"
SERVER_FILE = "properties/server.json"
QUERY_FILE = "properties/query.json"


################################ ENTRY POINT OF THE PROGRAM ################################
def main():

    args = sys.argv[1:]
    if not args:
        print(f"bad usage => {USAGE}")
        sys.exit(1)

    settings_string = ""
    # Extract arguments
    bot_name = args[0]
    sensor_type = args[1]

    # Create 'logger' and 'debugger' associated to 'bot_name'
    debugger = log.get_logger(use_color=True)
    logger = log.get_logger(log_filename=bot_name, log_sub_dir="log")

    try:

        # Get the 'bot_class' to use in the program
        bot_class = fact.get_bot_class(bot_name=bot_name, sensor_type=sensor_type)
        settings_string += f"success => bot_class={bot_class.__name__}, sensor_type={sensor_type}, "

        # Load '.env' file
        dotenv.load_dotenv(dotenv_path="./properties/.env")

        # Open database connection
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
            url_param['api_key'] = os.environ['PURPLEAIR_API_KEY']

        # TextParser class
        if sensor_type == 'purpleair':
            text_parser_class = txt.JSONParser
        else:
            if not url_param.get('format'):
                raise KeyError("bad 'api.json' file structure => missing key='format'")
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

        # API to Database UniformReshaper
        api2db_rshp_class = a2d.get_api2db_reshaper_class(sensor_type)
        settings_string += f"api2db_rshp_class={api2db_rshp_class.__name__}, "

        # Create the bot instance
        bot = bot_class(sensor_type=sensor_type, dbconn=dbconn)

        # Add external dependencies
        bot.add_url_builder(url_builder)
        bot.add_api_extractor_class(extractor_class)
        bot.add_api2db_rshp_class(api2db_rshp_class)
        bot.add_query_picker(query_picker)
        bot.add_text_parser_class(text_parser_class)

        if bot_name == 'init':
            bot.add_geom_builder_class(geom.PointBuilder)
            bot.add_current_ts(ts.CurrentTimestamp())

        # Database to API UniformReshaper
        if bot_name == 'fetch':
            db2api_rshp_class = d2a.get_db2api_reshaper_class(sensor_type)
            bot.add_db2api_rshp_class(db2api_rshp_class)
            settings_string += f"db2api_rshp_class={db2api_rshp_class.__name__}, "

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
        debugger.error(str(ex))
        sys.exit(1)
