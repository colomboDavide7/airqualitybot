#################################################
#
# @Author: davidecolombo
# @Date: lun, 18-10-2021, 12:29
# @Description: This script contains the 'main()' function,
#               i.e., the entry point for the application
#
#################################################
import sys
from typing import List, Dict, Any
from airquality.app.session import Session
from airquality.app.resource_loader import ResourceLoader
from airquality.bot.bot import BotMobile


USAGE = "USAGE: python -m airquality " \
        "[--help or -h | --debug  or -d | --log or -l] db_username"

RESOURCES  = "properties/resources.json"


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
    session.debug_msg(f"{main.__name__}(): session created successfully")
    session.debug_msg(str(session))

    # STEP 4 - create Resource Loader
    res_loader = ResourceLoader(path = RESOURCES, session = session)
    session.debug_msg(str(res_loader))

    # STEP 5 - load and parse resources
    try:
        res_loader.load_resources()
        res_loader.parse_resources()
    except SystemExit as ex:
        session.debug_msg(str(ex))
        sys.exit(1)

    # STEP 6 - create database connection interface
    try:
        session.debug_msg(f"{main.__name__}: get database connection")
        dbconn = res_loader.database_connection(username = current_user)
    except SystemExit as ex:
        session.debug_msg(str(ex))
        sys.exit(1)

    # STEP 7 - create bot based on username
    try:
        if current_user == 'bot_mobile_user':
            session.debug_msg(f"{main.__name__}: get sensor models for '{current_user}' user")
            models = res_loader.sensor_models("mobile")
            bot = BotMobile(dbconn, models)
            session.debug_msg(f"{main.__name__}: BotMobile created successfully")
        elif current_user == 'bot_station_user':
            models = res_loader.sensor_models("station")
            pass
    except SystemExit as ex:
        session.debug_msg(str(ex))
        sys.exit(1)
