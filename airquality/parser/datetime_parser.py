#################################################
#
# @Author: davidecolombo
# @Date: ven, 22-10-2021, 12:04
# @Description: this script defines a class for parsing sensor's API timestamps
#
#################################################
import datetime
import re
import builtins
from airquality.constants.shared_constants import EMPTY_STRING, \
    ATMOTUBE_DATETIME_REGEX_PATTERN, SQL_TIMESTAMP_REGEX_PATTERN, DATETIME2SQLTIMESTAMP_FORMAT


class DatetimeParser(builtins.object):


    @classmethod
    def today(cls) -> datetime.datetime:
        return datetime.datetime.today()


    @classmethod
    def date2string(cls, date: datetime.date) -> str:
        date_string = date.strftime('%Y-%m-%d')
        return date_string


    @classmethod
    def string2date(cls, date: str) -> datetime.datetime:
        date = datetime.datetime.strptime(date, "%Y-%m-%d")
        return date


    @classmethod
    def add_days_to_date(cls, date: datetime.datetime, days: int) -> datetime.datetime:
        new_date = date + datetime.timedelta(days = days)
        return new_date

    ################################ ATMOTUBE TIMESTAMP FORMATTING METHOD ################################


    @classmethod
    def atmotube_to_sqltimestamp(cls, ts: str) -> str:
        """Class method that takes atmotube timestamp and convert it into a valid SQL timestamp."""

        DatetimeParser._raise_system_exit_if_timestamp_does_not_match_pattern(ts = ts, pattern = ATMOTUBE_DATETIME_REGEX_PATTERN)
        ts = ts.strip('Z')
        ts, zone = ts.split('.')
        return ts.replace("T", " ")


################################ SQLTIMESTAMP FORMATTING METHODS ################################


    @classmethod
    def sqltimestamp_date(cls, ts: str):
        """Class method that takes a SQL timestamp and returns the date part."""

        DatetimeParser._raise_system_exit_if_timestamp_does_not_match_pattern(ts = ts, pattern = SQL_TIMESTAMP_REGEX_PATTERN)
        date, time = ts.split(" ")
        return date


    @classmethod
    def current_sqltimestamp(cls) -> str:
        """Class method that returns the current sql timestamp."""

        ts = datetime.datetime.now().strftime(DATETIME2SQLTIMESTAMP_FORMAT)
        return ts


################################ SQLTIMESTAMP COMPARISON METHOD ################################


    @classmethod
    def is_ts2_after_ts1(cls, ts1: str, ts2: str) -> bool:
        """Class method that compares if SQL timestamp 'ts2' comes after 'ts1' SQL timestamp.

        If EMPTY_STRING value is passed, return False.
        If invalid SQL timestamp format, SystemExit exception is raised."""

        if ts1 == EMPTY_STRING or ts2 == EMPTY_STRING:
            return False

        DatetimeParser._raise_system_exit_if_timestamp_does_not_match_pattern(ts = ts1, pattern = SQL_TIMESTAMP_REGEX_PATTERN)
        DatetimeParser._raise_system_exit_if_timestamp_does_not_match_pattern(ts = ts2, pattern = SQL_TIMESTAMP_REGEX_PATTERN)

        ts1_datetime = datetime.datetime.strptime(ts1, DATETIME2SQLTIMESTAMP_FORMAT)
        ts2_datetime = datetime.datetime.strptime(ts2, DATETIME2SQLTIMESTAMP_FORMAT)

        if (ts2_datetime - ts1_datetime).total_seconds() > 0:
            return True
        return False


################################ EXCEPTION METHOD ################################


    @classmethod
    def _raise_system_exit_if_timestamp_does_not_match_pattern(cls, ts: str, pattern: str) -> None:
        if not re.match(re.compile(pattern), ts):
            raise SystemExit(f"{DatetimeParser._raise_system_exit_if_timestamp_does_not_match_pattern.__name__}(): "
                             f"timestamp '{ts}' does not match regex patter '{pattern}'.")
