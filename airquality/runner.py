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


USAGE = "USAGE: python -m airquality " \
        "[--help or -h | --debug  or -d | --log or -l]"

RESOURCES  = "properties/resources.json"


def parse_sys_argv(args: List[str]) -> Dict[str, Any]:
    """Function that parses the command line arguments

    If the first argument is '-h' or '--help', the function will display the
    help for the application usage and then exit with status code 0.

    Otherwise it cycles through the list of arguments, creates a dict
    object that contains the only valid arguments and returns it.

    Unknown or invalid arguments are ignored.
    """
    if args[0] in ("--help", "-h"):
        print(USAGE)
        sys.exit(0)

    kwargs = {}

    for arg in args:
        if arg.startswith('-'):
            if arg in ("-d", "--debug"):
                kwargs["debug"] = True
            elif arg in ("-l", "--log"):
                kwargs["logging"] = True
            else:
                print(f"ignore invalid argument \'{arg}\'")
        else:
            print(f"ignore invalid argument \'{arg}\'")

    return kwargs

################################ MAIN FUNCTION ################################
def main() -> None:
    """This function is the entry point for the application

    {usage}

    The application expects two optional command line option-argument:
    1) --help or -h:  display help on program usage (MUST BE THE FIRST)
    2) --log or -l:   turn on local logging
    3) --debug or -d: run the application in debug mode
    """.format(usage = USAGE)

    args = sys.argv[1:]

    session_kwargs = {}
    if args:
        session_kwargs = parse_sys_argv(args)

    # STEP 1 - create Session object
    session = Session(session_kwargs)
    session.debug_msg("Session created successfully")
    session.debug_msg(str(session))

    # STEP 2 - create Resource Loader
    res_loader = ResourceLoader(path = RESOURCES, session = session)
    session.debug_msg(str(res_loader))

    # STEP 3 - open, read, close resource file
    try:
        res_loader.load_resources()
    except SystemExit as ex:
        session.debug_msg(str(ex))
        sys.exit(1)

    # STEP 4 - parse resources
    try:
        res_loader.parse_resources()
    except SystemExit as ex:
        session.debug_msg(str(ex))
        sys.exit(1)
