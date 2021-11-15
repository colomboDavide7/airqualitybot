######################################################
#
# Author: Davide Colombo
# Date: 15/11/21 08:43
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import os
import airquality.logger.log as log
import airquality.logger.fmt as log_fmt
import airquality.database.conn as db


################################ MAKE DEBUGGER FUNCTION ################################
def make_console_debugger(use_color=True):
    """Function that creates a Logger with a StreamHandler and a ColoredFormatter."""

    handler_cls = log.get_handler_cls(use_file=False)
    handler = handler_cls()
    fmt_cls = log_fmt.get_formatter_cls(use_color)
    fmt = fmt_cls(log_fmt.FMT_STR)
    return log.get_logger(handler=handler, formatter=fmt)


################################ MAKE LOGGER FUNCTION ################################
def make_file_logger(file_path: str, mode='a+'):
    """Function that creates a Logger instance with a FileHandler and a CustomFormatter."""

    handler_cls = log.get_handler_cls(use_file=True)
    handler = handler_cls(file_path, mode)
    fmt_cls = log_fmt.get_formatter_cls()
    fmt = fmt_cls(log_fmt.FMT_STR)
    return log.get_logger(handler=handler, formatter=fmt)


################################ MAKE DATABASE ADAPTER FUNCTION ################################
def make_database_adapter():
    """Function that checks if the 'DBCONN' key is present in the '.env' file, handles errors in case it will miss
    and return a database adapter object."""

    if not os.environ.get('DBCONN'):
        raise SystemExit(f"'{make_database_adapter.__name__}()': bad '.env' file structure => missing param='DBCONN'")
    return db.Psycopg2DatabaseAdapter(os.environ['DBCONN'])
