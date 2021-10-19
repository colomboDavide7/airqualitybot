#################################################
#
# @Author: davidecolombo
# @Date: mar, 19-10-2021, 08:58
# @Description: This file contains the application guard class
#
#################################################
import builtins
import os
import sys
from airquality.app.session import Session


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
