#################################################
#
# @Author: davidecolombo
# @Date: lun, 18-10-2021, 18:18
# @Description: this script defines a class that holds the current session state of the application.
#
#################################################
import builtins


class Session(builtins.object):
    """Session class represents the current session state of the application.

    - debug:    if True, print debug messages on the command line
    - logging:  if True, log event locally"""

    __current_session = None

    @staticmethod
    def get_current_session():
        if Session.__current_session is None:
            Session.__current_session = Session()
        return Session.__current_session

    DEBUG_HEADER = "[DEBUG]: "

    def __init__(self):
        self.__debug    = False
        self.__logging  = False

    @property
    def debug(self) -> bool:
        return self.__debug

    @debug.setter
    def debug(self, value: bool):
        self.__debug = value

    @property
    def logging(self) -> bool:
        return self.__logging

    @logging.setter
    def logging(self, value: bool):
        self.__logging = value

    def debug_msg(self, msg: str) -> bool:
        """This method print to the console the debug header followed by the 'msg' argument if debug mode is active."""

        if self.__debug:
            print(Session.DEBUG_HEADER + msg)
            return True
        return False

    def __str__(self):
        return f"{Session.__name__}: 'debug'={self.__debug}, 'logging'={self.__logging}"
