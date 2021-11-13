######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 10/11/21 19:52
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import logging


def get_handler_cls(use_file=False):
    handler = logging.StreamHandler
    if use_file:
        handler = logging.FileHandler
    return handler


def get_logger(handler: logging.Handler, formatter: logging.Formatter) -> logging.Logger:
    logger = logging.Logger(__name__)       # create logger with name='debugger'
    handler.setFormatter(formatter)         # add Formatter dependency to Handler
    logger.addHandler(handler)              # add Handler dependency to Logger
    logger.setLevel(logging.DEBUG)          # set logging level
    return logger
