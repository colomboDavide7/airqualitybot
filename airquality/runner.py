#################################################
#
# @Author: davidecolombo
# @Date: lun, 18-10-2021, 12:29
# @Description: This script contains the 'main()' function,
#               i.e., the entry point for the application
#
#################################################
import builtins
import os
import sys
from typing import List, Dict, Any

from airquality.app.session import Session

USAGE = "USAGE: python -m airquality " \
        "[--help or -h | --debug  or -d | --log or -l]"



def main() -> None:
    """This function is the entry point for the application

    {usage}

    The application expects two optional command line option-argument:
    1) --help or -h:  display help on program usage (MUST BE THE FIRST)
    2) --log or -l:   turn on local logging
    3) --debug or -d: run the application in debug mode
    """.format(usage = USAGE)

    global resource_path

    args = sys.argv[1:]

    session_kwargs = {}
    if args:
        session_kwargs = parse_sys_argv(args)

    # STEP 1 - create Session object
    session = Session(session_kwargs)
    if session.is_debug_active():
        session.debug_msg("Session created successfully")
        print(str(session))

    # STEP 2 - create AppGuard
    guard = AppGuard(session)

    # STEP 3 - get resource file path from the command line
    try:
        resource_path = get_resource_file_path(guard)
    except FileNotFoundError as ex:
        guard.sys_exit(str(ex), error_code = 1)
    except ValueError as ex:
        guard.sys_exit(str(ex), error_code = 1)

    # STEP 4 - set the Session resource file path
    session.set_res_path(resource_path)


    # TODO: create resource loader with singleton

    # TODO: read resource file

    # TODO: Create the Parse

    # TODO: parse the first file

    # TODO: ...


################################ APP GUARD ################################
class AppGuard(builtins.object):
    """This class defines the methods for controlling the flow of the
    application during the execution of main() method.

    The only argument that it takes is a Session object.
    """

    def __init__(self, session: Session):
        self.session = session

    def sys_exit(self, error_msg: str, error_code: int) -> None:
        """This function is called when an error occurs in the program.

        It shut down the python interpreter with status code equal to
        the 'status' argument
        """
        if self.session.is_debug_active():
            self.session.debug_msg(error_msg)
            self.session.debug_msg(f"Quit the Python interpreter: "
                                   f"error code = {error_code}")
        sys.exit(error_code)

    def is_valid_file_path(self, path: str) -> None:
        """
        This function checks if the path is a valid FILE path.
        """
        if not os.path.isfile(path):
            self.sys_exit(error_msg = f"File '{path}' is not a valid file path.",
                          error_code = 1)
        if self.session.is_debug_active():
            self.session.debug_msg("is valid file path?: ok")

    def is_resource_file_path(self, path: str) -> None:
        """
        This function checks if the path is a valid resource FILE path.
        """
        if "properties/resources.json" not in path:
            self.sys_exit(error_msg = f"File '{path}' is not a valid resource. "
                                      f"Please, read the "
                                      f"'instruction.txt' file in docs folder.",
                          error_code = 1)
        if self.session.is_debug_active():
            self.session.debug_msg("is resource file path?: ok")


def get_resource_file_path(guard: AppGuard) -> str:
    """
    This function ask to the user the resource file path and checks its
    correctness.

    See help(AppGuard.is_valid_file_path) & help(AppGuard.is_resource_file_path)
    for more info.
    """

    path_to_file = input("Enter resource file path: ")
    guard.is_valid_file_path(path_to_file)
    guard.is_resource_file_path(path_to_file)
    return path_to_file


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
