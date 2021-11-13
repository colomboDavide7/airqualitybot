######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 10/11/21 20:07
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import functools
import inspect
import os
import sys

import airquality.core.logger.log as log
import airquality.core.logger.fmt as formt


def log_decorator(_func=None):
    def log_decorator_info(func):
        @functools.wraps(func)
        def log_decorator_wrapper(self, *args, **kwargs):

            # Create 'logger'
            handler_cls = log.get_handler_cls(use_file=True)
            handler = handler_cls(f'log/{self.log_filename}.log', 'a+')
            fmt_cls = formt.get_formatter_cls(use_color=False)
            fmt = fmt_cls()
            logger_obj = log.get_logger(handler=handler, formatter=fmt)

            args_passed_in_function = [repr(arg) for arg in args]
            kwargs_passed_in_function = [f"{k}={v!r}" for k, v in kwargs.items()]
            formatted_arguments = ', '.join(args_passed_in_function + kwargs_passed_in_function)

            py_file_caller = inspect.getframeinfo(inspect.stack()[1][0])
            extra_args = {'func_name_override': func.__name__,
                          'file_name_override': os.path.basename(py_file_caller.filename)}
            logger_obj.info(f"Arguments: {formatted_arguments} - Begin function", extra=extra_args)
            try:
                value = func(self, *args, **kwargs)
                logger_obj.info(f"Returned: - End function {value!r}", extra=extra_args)
            except SystemExit:
                logger_obj.error(f"Exception: {str(sys.exc_info()[1])}", extra=extra_args)
                raise
            return value
        return log_decorator_wrapper
    if _func is None:
        return log_decorator_info
    else:
        return log_decorator_info(_func)
