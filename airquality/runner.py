#################################################
#
# @Author: davidecolombo
# @Date: lun, 18-10-2021, 12:29
# @Description: This script contains the 'main()' function, i.e., the entry point for the application
#
#################################################
import sys
from typing import List, Dict, Any
from airquality.io.io import IOManager
from airquality.bot.bot import BotMobile
from airquality.app.session import Session
from airquality.parser.file_parser import FileParserFactory
from airquality.database.sql_query_builder import SQLQueryBuilder
from airquality.picker.resource_picker import ResourcePicker
from airquality.database.db_conn_adapter import DatabaseConnectionAdapterFactory


USAGE = "USAGE: python -m airquality " \
        "[--help or -h | --debug  or -d | --log or -l] db_username"

RESOURCES  = "properties/resources.json"
QUERIES    = "properties/sql_query.json"


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
    is_username_set = False

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
            if not is_username_set:
                kwargs["username"] = arg
                is_username_set = True
            else:
                print(f"{parse_sys_argv.__name__}: "
                      f"ignore invalid option '{arg}'.")

    if not is_username_set:
        raise SystemExit(f"{parse_sys_argv.__name__}: "
                         f"missing required username for database connection.")
    return kwargs


################################ MAIN FUNCTION ################################
def main() -> None:
    """This function is the entry point for the application

    {usage}

    The application expects two optional command line option-argument:
    1) --help or -h:  display help on program usage (MUST BE THE FIRST)
    2) --log or -l:   turn on local logging
    3) --debug or -d: run the application in debug mode
    4) db_username:   the username that you want to connect with to the database
    """.format(usage = USAGE)

    args = sys.argv[1:]
    # STEP 1 - check if args are empty and if it is, raise SystemExit
    if not args:
        print(USAGE)
        sys.exit(1)

    # STEP 2 - parse args and pop username
    session_kwargs = parse_sys_argv(args)
    current_user = session_kwargs.pop("username")

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

        # STEP 6 - create database connection interface
        dbconn_factory = DatabaseConnectionAdapterFactory()
        settings = ResourcePicker.pick_db_conn_properties_from_user(
                parsed_resources = parsed_resources,
                username = current_user
        )
        session.debug_msg(f"{main.__name__}(): try to instantiate database settings: OK")
        dbconn = dbconn_factory.create_connection(settings)
        session.debug_msg(f"{main.__name__}(): try to instantiate database connection adapter: OK")

        # STEP 7 - create sql query builder
        query_builder = SQLQueryBuilder(query_file_path = QUERIES)
        session.debug_msg(f"{main.__name__}(): try to instantiate sql query builder: OK")

        if current_user == 'bot_mobile_user':
            models = ResourcePicker.pick_sensor_models_from_sensor_type(
                    parsed_resources = parsed_resources,
                    sensor_type = "mobile"
            )
            bot = BotMobile(dbconn = dbconn, query_builder = query_builder, sensor_models = models)
            session.debug_msg(f"{main.__name__}(): try to instantiate mobile bot: OK")

        elif current_user == 'bot_station_user':
            pass

    except SystemExit as ex:
        session.debug_msg(str(ex))
        sys.exit(1)
