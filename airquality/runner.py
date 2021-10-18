#################################################
#
# @Author: davidecolombo
# @Date: lun, 18-10-2021, 12:29
# @Description: This script contains the 'main()' function,
#               i.e., the entry point for the application
#
#################################################
import sys, os
from typing import List, Dict, Any
from airquality.app.session import Session

# Imported for input() function in 'tests.runner.test_runner.py'
# DO NOT DELETE
import builtins

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

    # STEP 1 - create Session object
    session = Session(session_kwargs)
    if session.is_debug_active():
        session.debug_msg("Session created successfully")

    # STEP 2 - get resource file path from the command line
    resource_path = None
    try:
        resource_path = get_resource_file_path()
        if session.is_debug_active():
            session.debug_msg("valid resource path")
    except FileNotFoundError as ex:
        if session.is_debug_active():
            session.debug_msg(str(ex))
            session.debug_msg("Quitting the application.")
        sys.exit(1)
    except ValueError as ex:
        if session.is_debug_active():
            session.debug_msg(str(ex))
            session.debug_msg("Quitting the application.")
        sys.exit(1)

    # TODO: create resource loader with singleton


    # TODO: read resource file


    # TODO: Create the Parse


    # TODO: parse the first file


    # TODO: ...



def get_resource_file_path() -> str:
    """Function that takes the path from the console user input,
    checks whether the provided path is a valid file and if
    the file is the correct one."""

    path_to_file = input("Enter resource file path: ")
    check_is_valid_file(path_to_file)
    check_resource_file_path(path_to_file)
    return path_to_file

def check_is_valid_file(path: str):
    if not os.path.isfile(path):
        raise FileNotFoundError(f"path to file '{path}' is not a valid.")

def check_resource_file_path(path: str):
    if "properties/resources.json" not in path:
        raise ValueError(f"Path to file {path} is wrong.")


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
