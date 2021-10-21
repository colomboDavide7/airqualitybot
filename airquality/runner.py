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
from airquality.database.sql_query_builder import SQLQueryBuilder
from airquality.picker.resource_picker import ResourcePicker
from airquality.database.db_conn_adapter import Psycopg2ConnectionAdapterFactory


USAGE = "USAGE: python -m airquality " \
        "[--help or -h | --debug  or -d | --log or -l] personality"

RESOURCES  = "properties/resources.json"
QUERIES    = "properties/sql_query.json"
VALID_PERSONALITY = ('atmotube', 'purpleair')


def parse_sys_argv(args: List[str]) -> Dict[str, Any]:
    """
    Function that parses the command line arguments

    If '-h' or '--help' is passed as first argument, the function will display
    the usage string and then exits with status code 0.

    If not username is provided, SystemExit exception is raised.

    Unknown or invalid arguments are ignored.
    """

    if args[0] in ("--help", "-h"):
        print(USAGE)
        sys.exit(0)

    kwargs = {}
    is_personality_set = False

    for arg in args:
        if arg.startswith('-'):
            if arg in ("-d", "--debug"):
                kwargs["debug"] = True
            elif arg in ("-l", "--log"):
                kwargs["logging"] = True
            else:
                print(f"{parse_sys_argv.__name__}: "
                      f"ignore invalid option '{arg}'.")
        else:
            if not is_personality_set:
                kwargs["personality"] = arg
                is_personality_set = True
            else:
                print(f"{parse_sys_argv.__name__}: "
                      f"ignore invalid option '{arg}'.")

    if not is_personality_set:
        raise SystemExit(f"{parse_sys_argv.__name__}: "
                         f"missing required bot personality for database connection.")
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
    """.format(usage = USAGE)

    args = sys.argv[1:]
    # STEP 1 - check if args are empty and if it is, raise SystemExit
    if not args:
        print(USAGE)
        sys.exit(1)

    # STEP 2 - parse args and pop personality
    session_kwargs = parse_sys_argv(args)
    bot_personality = session_kwargs.pop("personality")

    if bot_personality not in VALID_PERSONALITY:
        print(f"{main.__name__}(): invalid personality. Choose one within {VALID_PERSONALITY}.")
        sys.exit(1)

    # STEP 3 - create Session object
    session = Session(session_kwargs)
    print(str(session))

    try:
        # STEP 4 - read resource file
        raw_resources = IOManager.open_read_close_file(path = RESOURCES)
        session.debug_msg(f"{main.__name__}(): try to read resource file at '{RESOURCES}': OK")

        # STEP 5 - parse raw resources
        parser = FileParserFactory.file_parser_from_file_extension(file_extension = RESOURCES.split('.')[-1])
        parsed_resources = parser.parse(raw_resources)
        session.debug_msg(f"{main.__name__}(): try to parse raw resources: OK")

        # STEP 6 - create psycopg2 connection adapter factory
        db_conn_factory = Psycopg2ConnectionAdapterFactory()

        # STEP 7 - pick database connection adapter properties from username
        properties = ResourcePicker.pick_db_conn_properties_from_personality(
                parsed_resources = parsed_resources,
                bot_personality = bot_personality
        )
        session.debug_msg(f"{main.__name__}(): try to pick database connection properties: OK")

        # STEP 8 - create psycopg2 connection adapter
        dbconn = db_conn_factory.create_database_connection_adapter(properties)
        session.debug_msg(f"{main.__name__}(): try to instantiate psycopg2 connection adapter: OK")

        # STEP 9 - create sql query builder
        query_builder = SQLQueryBuilder(query_file_path = QUERIES)
        session.debug_msg(f"{main.__name__}(): try to instantiate sql query builder: OK")

        # STEP 10 - create bot from personality
        bot = BotFactory.create_bot_from_personality(bot_personality = bot_personality)
        session.debug_msg(f"{main.__name__}(): try to instantiate bot from personality '{bot_personality}': OK")


    except SystemExit as ex:
        session.debug_msg(str(ex))
        sys.exit(1)
