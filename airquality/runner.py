#################################################
#
# @Author: davidecolombo
# @Date: lun, 18-10-2021, 12:29
# @Description: this script defines the functions for parsing application arguments and 'main()'.
#
#################################################
import sys
from typing import List, Dict, Any
from airquality.io.io import IOManager
from airquality.bot.bot import BotFactory
from airquality.app.session import Session
from airquality.parser.file_parser import FileParserFactory
from airquality.picker.resource_picker import ResourcePicker
from airquality.api.api_request_adapter import APIRequestAdapter
from airquality.database.sql_query_builder import SQLQueryBuilder
from airquality.database.db_conn_adapter import Psycopg2ConnectionAdapterFactory


USAGE = "USAGE: python -m airquality " \
        "[--help or -h | --debug  or -d | --log or -l] personality api_address_number"

RESOURCES  = "properties/resources.json"
QUERIES    = "properties/sql_query.json"
VALID_PERSONALITY = ('atmotube', 'purpleair')


def parse_sys_argv(args: List[str]) -> Dict[str, Any]:
    """
    Function that parses the command line arguments

    If '-h' or '--help' is passed as first argument, the function will display
    the usage string and then exits with status code 0.

    If not personality is provided, SystemExit exception is raised.

    If not api_address_number is provided, SystemExit exception is raised.

    Unknown or invalid arguments are ignored.
    """

    if args[0] in ("--help", "-h"):
        print(USAGE)
        sys.exit(0)

    kwargs = {}
    is_personality_set = False
    is_api_address_number_set = False

    for arg in args:
        if arg.startswith('-'):
            if arg in ("-d", "--debug"):
                kwargs["debug"] = True
            elif arg in ("-l", "--log"):
                kwargs["logging"] = True
            else:
                print(f"{parse_sys_argv.__name__}: ignore invalid option '{arg}'.")
        else:
            if not is_personality_set and arg in VALID_PERSONALITY:
                kwargs["personality"] = arg
                is_personality_set = True
            elif not is_api_address_number_set and arg.isdigit():
                kwargs["api_address_number"] = arg
                is_api_address_number_set = True
            else:
                print(f"{parse_sys_argv.__name__}: ignore invalid option '{arg}'.")

    if not is_personality_set:
        raise SystemExit(f"{parse_sys_argv.__name__}(): missing required bot personality.")

    if not is_api_address_number_set:
        raise SystemExit(f"{parse_sys_argv.__name__}(): missing required api address number.")

    return kwargs


################################ MAIN FUNCTION ################################
def main() -> None:
    """This function is the entry point for the application

    {usage}

    The application expects two optional command line option-argument:
    1) --help or -h:  display help on program usage (MUST BE THE FIRST)
    2) --log or -l:   turn on local logging
    3) --debug or -d: run the application in debug mode
    4) personality:   the bot personality for connecting to APIs and database
    5) api address number: the api address number from the 'api_address' section in the resource file
    """.format(usage = USAGE)

    args = sys.argv[1:]
    if not args:
        print(USAGE)
        sys.exit(1)

    session_kwargs = parse_sys_argv(args)
    bot_personality = session_kwargs.pop("personality")
    api_address_number = session_kwargs.pop("api_address_number")

    session = Session(session_kwargs)
    print(str(session))

    session.debug_msg(f"{main.__name__}(): -------- STARTING THE PROGRAM --------")
    try:
        # GET RAW RESOURCE FROM FILE
        raw_resources = IOManager.open_read_close_file(path = RESOURCES)
        session.debug_msg(f"{main.__name__}(): try to read resource file at '{RESOURCES}': OK")

        # PARSE RESOURCE
        parser = FileParserFactory.file_parser_from_file_extension(file_extension = RESOURCES.split('.')[-1])
        parsed_resources = parser.parse(raw_resources)
        session.debug_msg(f"{main.__name__}(): try to parse raw resources: OK")

        # GET DATABASE CONNECTION PROPERTIES FROM BOT PERSONALITY
        properties = ResourcePicker.pick_db_conn_properties_from_personality(
                parsed_resources = parsed_resources,
                bot_personality = bot_personality
        )
        session.debug_msg(f"{main.__name__}(): try to pick database connection properties: OK")

        # GET API ADDRESS FROM BOT PERSONALITY AND API ADDRESS NUMBER
        api_address = ResourcePicker.pick_api_address_from_number(
                parsed_resources = parsed_resources,
                bot_personality = bot_personality,
                api_address_number = api_address_number
        )
        session.debug_msg(f"{main.__name__}(): try to pick api address for personality '{bot_personality}' "
                          f"with number '{api_address_number}': OK")

        # CREATE DATABASE ADAPTER
        db_conn_factory = Psycopg2ConnectionAdapterFactory()
        dbconn = db_conn_factory.create_database_connection_adapter(properties)
        session.debug_msg(f"{main.__name__}(): try to instantiate psycopg2 connection adapter: OK")

        # CREATE QUERY BUILDER
        query_builder = SQLQueryBuilder(query_file_path = QUERIES)
        session.debug_msg(f"{main.__name__}(): try to instantiate sql query builder: OK")

        # GET API ADAPTER
        api_adapter = APIRequestAdapter(api_address = api_address)
        session.debug_msg(f"{main.__name__}(): try to instantiate api adapter with address '{api_address}': OK")

        # CREATE BOT FROM BOT PERSONALITY
        bot = BotFactory.create_bot_from_personality(bot_personality = bot_personality)
        session.debug_msg(f"{main.__name__}(): try to instantiate bot from personality '{bot_personality}': OK")

        # SET QUERY BUILDER TO BOT
        bot.sqlbuilder = query_builder
        session.debug_msg(f"{main.__name__}(): try to set query builder to bot: OK")

        # SET DATABASE ADAPTER TO BOT
        bot.dbconn = dbconn
        session.debug_msg(f"{main.__name__}(): try to set database connection adapter to bot: OK")

        # SET API ADAPTER TO BOT
        bot.apiadapter = api_adapter
        session.debug_msg(f"{main.__name__}(): try to set api adapter to bot: OK")

    except SystemExit as ex:
        session.debug_msg(str(ex))
        sys.exit(1)

    session.debug_msg(f"{main.__name__}(): -------- PROGRAM ENDS WITH SUCCESS --------")
