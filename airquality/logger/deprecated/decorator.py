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

import airquality.logger.fact as logfact

FORMATTED_ARGUMENTS_MAX_LEN = 50


def log_decorator(_func=None):
    def log_decorator_info(func):
        @functools.wraps(func)
        def log_decorator_wrapper(self, *args, **kwargs):

            # Create file logger
            logger_obj = logfact.get_file_logger(file_path=f"log/{self.log_filename}.log", mode='a+', logger_name=f"file_{__name__}")
            debugger_obj = logfact.get_console_logger(use_color=True, logger_name=f"console_{__name__}")

            # Get the file caller
            py_file_caller = inspect.getframeinfo(inspect.stack()[1][0])
            extra_args = {'func_name_override': func.__name__,
                          'file_name_override': os.path.basename(py_file_caller.filename)}

            # Get function args and kwargs in the proper shape
            function_args = [repr(a) for a in args]
            function_kwargs = [f"{k}={v!r}" for k, v in kwargs.items()]
            formatted_arguments = ', '.join(function_args + function_kwargs)

            # Trim the formatted_arguments if they are too long
            if len(formatted_arguments) >= FORMATTED_ARGUMENTS_MAX_LEN:
                formatted_arguments = formatted_arguments[0:25] + " ... " + formatted_arguments[-25:-1]

            # Log CALL to function
            logger_obj.debug(f"=> CALL {func.__name__}({formatted_arguments}) in {self.__class__.__name__}", extra=extra_args)
            debugger_obj.debug(f"=> CALL {func.__name__}({formatted_arguments}) in {self.__class__.__name__}", extra=extra_args)
            try:
                value = func(self, *args, **kwargs)
                logger_obj.debug(f"<= RETURN from {func.__name__}() in {self.__class__.__name__}", extra=extra_args)
                debugger_obj.debug(f"<= RETURN from {func.__name__}() in {self.__class__.__name__}", extra=extra_args)
            except SystemExit:
                logger_obj.error(f"<= EXCEPTION: {str(sys.exc_info()[1])}", extra=extra_args)
                raise
            return value
        return log_decorator_wrapper
    if _func is None:
        return log_decorator_info
    else:
        return log_decorator_info(_func)
