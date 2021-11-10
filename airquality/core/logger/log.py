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


def get_logger(log_filename: str, log_sub_dir: str = "log") -> logging.Logger:

    log_path = log_filename if os.path.exists(log_filename) else os.path.join(log_sub_dir, (str(log_filename)))
    logger = logging.Logger(log_filename)
    handler = logging.FileHandler(log_path, 'a+')
    formatter = CustomFormatter('[%(asctime)s - %(levelname)s]: %(filename)s - %(funcName)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger


class CustomFormatter(logging.Formatter):

    def format(self, record) -> str:
        if hasattr(record, 'func_name_override'):
            record.funcName = record.func_name_override
        if hasattr(record, 'file_name_override'):
            record.filename = record.file_name_override
        return super(CustomFormatter, self).format(record)
