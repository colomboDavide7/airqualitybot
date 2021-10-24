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


    @staticmethod
    def parse_atmotube_timestamp(ts: str) -> str:
        if not re.match(DatetimeParser.ATMOTUBE_DATETIME_PATTERN, ts):
            raise SystemExit(f"{DatetimeParser.parse_atmotube_timestamp.__name__}(): "
                             f"cannot parse invalid Atmotube timestamp.")
        ts = ts.strip('Z')
        ts, zone = ts.split('.')
        return ts.replace("T", " ")


    @staticmethod
    def split_last_atmotube_measure_timestamp_from_api_param(last_atmotube_timestamp: str):
        date = ""
        time = ""
        if last_atmotube_timestamp:
            date, time = last_atmotube_timestamp.split(" ")
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
