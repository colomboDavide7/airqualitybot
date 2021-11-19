######################################################
#
# Author: Davide Colombo
# Date: 10/11/21 20:07
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import functools
import inspect
import os
import sys

import airquality.logger.util.log as make


def log_decorator(_func=None):
    def log_decorator_info(func):
        @functools.wraps(func)
        def log_decorator_wrapper(self, *args, **kwargs):

            # Create file logger
            logger_obj = make.get_file_logger(file_path=f"log/{self.log_filename}.log", mode='a+', logger_name=f"file_{__name__}")
            debugger_obj = make.get_console_logger(use_color=True, logger_name=f"console_{__name__}")

            # Get the file caller
            py_file_caller = inspect.getframeinfo(inspect.stack()[1][0])
            extra_args = {'func_name_override': func.__name__,
                          'file_name_override': os.path.basename(py_file_caller.filename)}

            logger_obj.debug(f"=> CALL on {self.__class__.__name__}", extra=extra_args)
            debugger_obj.debug(f"=> CALL on {self.__class__.__name__}", extra=extra_args)
            try:
                value = func(self, *args, **kwargs)
                logger_obj.debug(f"<= RETURN from {self.__class__.__name__}", extra=extra_args)
                debugger_obj.debug(f"<= RETURN from {self.__class__.__name__}", extra=extra_args)
            except SystemExit:
                logger_obj.error(20*'x' + f" Exception: {str(sys.exc_info()[1])} " + 20*'x', extra=extra_args)
                raise
            return value
        return log_decorator_wrapper
    if _func is None:
        return log_decorator_info
    else:
        return log_decorator_info(_func)


# logger_obj.debug(20*"-" + f" CALL " + 20*"-", extra=extra_args)
#             debugger_obj.debug(20*"-" + f" CALL " + 20*"-", extra=extra_args)
