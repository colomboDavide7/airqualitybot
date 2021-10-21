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

    - debug:    if True, print debug messages on the command line
    - logging:  if True, log event locally
    """

    DEBUG_HEADER = "[DEBUG]: "

    def __init__(self, settings: Dict[str, Any]):
        self.__debug    = False
        self.__logging  = False

        if settings:
            for key, val in settings.items():
                if key == 'debug':
                    self.__debug = True
                elif key == 'logging':
                    self.__logging = True

    @property
    def debug(self):
        return self.__debug

    @property
    def logging(self):
        return self.__logging

    def debug_msg(self, msg: str) -> bool:
        """This method print to the console the debug header followed by
        the debug message passed as argument if debug mode is active."""
        if self.__debug:
            print(Session.DEBUG_HEADER + msg)
            return True
        return False

    def __str__(self):
        return f"{Session.__name__}: 'debug'={self.__debug}, 'logging'={self.__logging}"
