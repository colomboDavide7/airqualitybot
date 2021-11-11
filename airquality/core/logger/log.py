######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 10/11/21 19:52
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import os
import logging

GREEN = "\033[1;32m"
BLUE = "\033[1;34m"
YELLOW = "\033[1;33m"
RED = "\033[1;31m"
RESET = "\033[0m"

COLORED_LEVELS = {'DEBUG': GREEN,
                  'INFO': BLUE,
                  'WARNING': YELLOW,
                  'ERROR': RED}


def get_logger(log_filename: str = "", log_sub_dir: str = "", use_color=False) -> logging.Logger:
    """Return a logger that outputs messages on the console or in a file."""

    # Define the 'logger_name' equal to module name if user leave it empty, otherwise use the 'log_filename'
    logger_name = __name__ if not log_filename else log_filename

    # Create a new 'logger'
    logger = logging.Logger(logger_name)

    # By default, logger outputs messages on the console
    handler = logging.StreamHandler()

    # If user provide a consistent path, then log to the file
    if log_filename:
        log_path = os.path.join(log_sub_dir, (str(log_filename) + '.log'))
        handler = logging.FileHandler(log_path, 'a+')

    formatter = CustomFormatter(f'[%(levelname)s] %(asctime)-30s %(filename)-25s %(funcName)-15s %(message)s')
    if use_color:
        formatter = ColoredFormatter(f'[%(levelname)s] %(asctime)-30s %(filename)-25s %(funcName)-15s %(message)s')

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger


class CustomFormatter(logging.Formatter):
    """Custom formatter for changing the name of the file and calling function."""

    def format(self, record) -> str:
        if hasattr(record, 'func_name_override'):
            record.funcName = record.func_name_override
        if hasattr(record, 'file_name_override'):
            record.filename = record.file_name_override
        return super(CustomFormatter, self).format(record)


class ColoredFormatter(logging.Formatter):

    def format(self, record) -> str:
        levelname = record.levelname
        if levelname in COLORED_LEVELS:
            colored_levelname = COLORED_LEVELS[levelname] + levelname + RESET
            record.levelname = colored_levelname
        return super(ColoredFormatter, self).format(record)
