######################################################
#
# Author: Davide Colombo
# Date: 10/11/21 19:52
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import logging
import airquality.logger.util.fmt as log_fmt


################################ CONSOLE LOGGER ################################
def get_console_logger(use_color=True, logger_name="debugger"):
    """Function that creates a Logger with a StreamHandler and a ColoredFormatter."""

    handler_cls = _get_handler_cls(use_file=False)
    handler = handler_cls()
    fmt_cls = log_fmt.get_formatter_cls(use_color)
    fmt = fmt_cls(log_fmt.FMT_STR)
    return _get_logger(handler=handler, formatter=fmt, logger_name=logger_name)


################################ FILE LOGGER ################################
def get_file_logger(file_path: str, mode='a+', logger_name="logger"):
    """Function that creates a Logger instance with a FileHandler and a CustomFormatter."""

    handler_cls = _get_handler_cls(use_file=True)
    handler = handler_cls(file_path, mode)
    fmt_cls = log_fmt.get_formatter_cls()
    fmt = fmt_cls(log_fmt.FMT_STR)
    return _get_logger(handler=handler, formatter=fmt, logger_name=logger_name)


################################ PROTECTED FUNCTIONS ################################
def _get_handler_cls(use_file=False):
    handler = logging.StreamHandler
    if use_file:
        handler = logging.FileHandler
    return handler


def _get_logger(handler: logging.Handler, formatter: logging.Formatter, logger_name: str) -> logging.Logger:
    logger = logging.getLogger(logger_name)     # create logger with name='debugger'
    handler.setFormatter(formatter)             # add Formatter dependency to Handler
    logger.addHandler(handler)                  # add Handler dependency to Logger
    logger.setLevel(logging.DEBUG)              # set logging level
    return logger
