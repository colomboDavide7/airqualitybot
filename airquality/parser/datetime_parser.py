#################################################
#
# @Author: davidecolombo
# @Date: ven, 22-10-2021, 12:04
# @Description: this script defines a class for parsing sensor's API timestamps
#
#################################################
import re
import builtins
from typing import Dict, Any, List
from airquality.picker import TIMESTAMP


class DatetimeParser(builtins.object):


    ATMOTUBE_DATETIME_PATTERN = re.compile(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d+Z')
    SQL_TIMESTAMP_PATTERN = re.compile(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')


    @staticmethod
    def _raise_system_exit_when_bad_atmotube_timestamp_occurs(ts: str, pattern):
        if not re.match(pattern, ts):
            raise SystemExit(f"{DatetimeParser._raise_system_exit_when_bad_atmotube_timestamp_occurs.__name__}(): "
                             f"cannot parse invalid timestamp.")

    @staticmethod
    def parse_atmotube_timestamp(ts: str) -> str:

        DatetimeParser._raise_system_exit_when_bad_atmotube_timestamp_occurs(
                ts = ts,
                pattern = DatetimeParser.ATMOTUBE_DATETIME_PATTERN
        )
        ts = ts.strip('Z')
        ts, zone = ts.split('.')
        return ts.replace("T", " ")


    @staticmethod
    def split_last_atmotube_measure_timestamp_from_api_param(ts: str):

        DatetimeParser._raise_system_exit_when_bad_atmotube_timestamp_occurs(
                ts = ts,
                pattern = DatetimeParser.SQL_TIMESTAMP_PATTERN
        )
        date, time = ts.split(" ")
        return date, time


    @staticmethod
    def last_timestamp_from_packets(packets: List[Dict[str, Any]]) -> str:

        packet_id = 0
        last_timestamp = ""

        for packet in packets:
            packet_id += 1
            if packet_id == len(packets):
                last_timestamp = packet[TIMESTAMP]

        return last_timestamp
