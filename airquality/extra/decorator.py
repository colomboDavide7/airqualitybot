# ======================================
# @author:  Davide Colombo
# @date:    2022-02-3, gio, 15:38
# ======================================
import logging
import functools


def log_context(logger_name: str, header: str, teardown: str):
    _logging = logging.getLogger(logger_name)

    def log_context_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            _logging.info(header)
            value = func(*args, **kwargs)
            _logging.info(teardown)
            return value
        return wrapper
    return log_context_decorator
