#################################################
#
# @Author: davidecolombo
# @Date: lun, 18-10-2021, 18:18
# @Description: this file defines the Session class and its behaviour
#
#################################################
import builtins


class Session(builtins.object):

    debug = False
    logging = False
    log_path = None
    username = None
    password = None

    def __init__(self, **kwargs):
        if kwargs:
            for key, val in kwargs.items():
                if key == 'debug':
                    self.debug = True
                elif key == 'logging':
                    self.logging = True


    def is_debug_active(self) -> bool:
        return self.debug == True

    def is_logging_active(self) -> bool:
        return self.logging == True
