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
from typing import Dict, Any, List
from airquality.constants.shared_constants import EMPTY_STRING, EMPTY_LIST, PICKER2SQLBUILDER_TIMESTAMP, \
    ATMOTUBE_DATETIME_REGEX_PATTERN, SQL_TIMESTAMP_REGEX_PATTERN, DATETIME2SQLTIMESTAMP_FORMAT


class DatetimeParser(builtins.object):


    @classmethod
    def _raise_system_exit_if_timestamp_does_not_match_pattern(cls, ts: str, pattern: str) -> None:
        if not re.match(re.compile(pattern), ts):
            raise SystemExit(f"{DatetimeParser._raise_system_exit_if_timestamp_does_not_match_pattern.__name__}(): "
                             f"timestamp '{ts}' does not match regex patter '{pattern}'.")


    @classmethod
    def atmotube_to_sqltimestamp(cls, ts: str) -> str:
        """Static method that takes atmotube timestamp and convert it into a valid SQL timestamp."""
        DatetimeParser._raise_system_exit_if_timestamp_does_not_match_pattern(ts = ts, pattern = ATMOTUBE_DATETIME_REGEX_PATTERN)
        ts = ts.strip('Z')
        ts, zone = ts.split('.')
        return ts.replace("T", " ")


    @classmethod
    def sqltimestamp_date(cls, ts: str):
        """Static method that takes a SQL timestamp and returns the date part."""

        DatetimeParser._raise_system_exit_if_timestamp_does_not_match_pattern(ts = ts, pattern = SQL_TIMESTAMP_REGEX_PATTERN)
        date, time = ts.split(" ")
        return date


    @classmethod
    def is_ts2_after_ts1(cls, ts1: str, ts2: str) -> bool:
        """Static method that compares if SQL timestamp 'ts2' is after 'ts1' SQL timestamp.

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


    @classmethod
    def last_packet_timestamp(cls, packets: List[Dict[str, Any]]) -> str:
        """Static method that returns the last packet timestamp taken from the 'packets' list.

        If the packet is equal to EMPTY_LIST, EMPTY_STRING timestamp is returned.

        If PICKER2SQLBUILDER_TIMESTAMP field is missing in last packets, SystemExit exception is raised."""

        last_timestamp = EMPTY_STRING
        if packets == EMPTY_LIST:
            return last_timestamp

        last_packet = packets[-1]
        if PICKER2SQLBUILDER_TIMESTAMP not in last_packet.keys():
            raise SystemExit(f"{DatetimeParser.last_packet_timestamp.__name__}: "
                             f"missing required argument '{PICKER2SQLBUILDER_TIMESTAMP}'.")
        return last_packet[PICKER2SQLBUILDER_TIMESTAMP]


    @classmethod
    def current_sqltimestamp(cls) -> str:
        """Static method that returns the current sql timestamp."""

        ts = datetime.datetime.now().strftime(DATETIME2SQLTIMESTAMP_FORMAT)
        return ts
