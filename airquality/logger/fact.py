######################################################
#
# Author: Davide Colombo
# Date: 10/11/21 19:52
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import logging
import airquality.logger.fmt as log_fmt

LOG_TYPE = logging.Logger


################################ shutdown() ################################
def shutdown():
    logging.shutdown()


################################ get_console_logger() ################################
def get_console_logger(use_color=True, logger_name="debugger", level=logging.DEBUG):
    handler = logging.StreamHandler()
    fmt = log_fmt.get_formatter(use_color)
    return _get_logger(handler=handler, formatter=fmt, logger_name=logger_name, level=level)


################################ get_file_logger() ################################
def get_file_logger(file_path: str, mode='a+', logger_name="logger", level=logging.DEBUG):
    handler = logging.FileHandler(filename=file_path, mode=mode)
    fmt = log_fmt.get_formatter()
    return _get_logger(handler=handler, formatter=fmt, logger_name=logger_name, level=level)


################################ _get_logger() ################################
def _get_logger(handler: logging.Handler, formatter: logging.Formatter, logger_name: str, level=logging.DEBUG) -> logging.Logger:
    logger = logging.Logger(logger_name)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)
    return logger
