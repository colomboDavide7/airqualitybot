#################################################
#
# @Author: davidecolombo
# @Date: lun, 18-10-2021, 18:18
# @Description: this file defines the Session class and its behaviour
#
#################################################
import builtins
from typing import Dict, Any


class Session(builtins.object):
    """Session class represents the current session state of the application.

    - debug:    if True, print debug message on the command line
    - logging:  if True, log event locally
    - log_path: path to the log file
    - username: current session's username, used for DB connection
    - password: current session's password, used for DB connection
    """

    DEBUG_HEADER = "[DEBUG]: "

    def __init__(self, settings: Dict[str, Any]):
        """
        __init__ method unpack the command line option-arguments
        passed in the form of a dictionary and sets the proper values.
        """
        self.__debug = False
        self.__logging = False
        self.__log_path = None
        self.__username = None
        self.__password = None

        if settings:
            for key, val in settings.items():
                if key == 'debug':
                    self.__debug = True
                elif key == 'logging':
                    self.__logging = True

    def debug_msg(self, msg: str) -> bool:
        """
        This method print to the console the debug header followed by
        the debug message passed as argument if debug mode is active.
        """
        if self.__debug:
            print(Session.DEBUG_HEADER + msg)
            return True
        return False

    def is_debug_active(self) -> bool:
        """
        return True if debug mode is active
        """
        return self.__debug

    def is_logging_active(self) -> bool:
        """
        return True if logging on the local file system is active
        """
        return self.__logging
