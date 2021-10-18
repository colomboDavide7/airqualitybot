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


USAGE = "python -m airquality [--help or -h | --debug  or -d | --log or -l]"

def main() -> None:
    """This function is the entry point for the application

    USAGE: {usage}

    The application expects two optional command line option-argument:
    1) --help or -h:  display help on program usage (MUST BE THE FIRST)
    2) --log or -l:   turn on local logging
    3) --debug or -d: run the application in debug mode
    """.format(usage=USAGE)

    args = sys.argv[1:]

    session_kwargs = {}
    if args:
        session_kwargs = parse_sys_argv(args)

    # TODO: create session object
    session = Session(session_kwargs)

    if session.is_debug_active():
        print("[DEBUG]: SESSION CREATED SUCCESSFULLY")

    # TODO: pass option-arguments to Session object



def parse_sys_argv(args: List[str]) -> Dict[str, Any]:
    """Function that parses the command line arguments

    If the first argument is '-h' or '--help', the function will display the
    help for the application usage and the exit with status code 0.

    Otherwise it cycles through the list of arguments and creates a dict
    object and returns it.
    """
    if args[0] in ("--help", "-h"):
        print("\nUSAGE: " + USAGE + "\n")
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
