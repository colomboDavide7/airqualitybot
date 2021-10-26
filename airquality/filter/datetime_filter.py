#################################################
#
# @Author: davidecolombo
# @Date: mar, 26-10-2021, 12:52
# @Description: this script defines the classes for filtering packets by acquisition time
#
#################################################
import builtins
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from airquality.parser.datetime_parser import DatetimeParser
from airquality.constants.shared_constants import EMPTY_STRING, EMPTY_LIST, \
    ATMOTUBE_TIME_PARAM


class DatetimeFilter(ABC):


    @abstractmethod
    def filter_packets(self, packets: List[Dict[str, Any]], sqltimestamp: str) -> List[Dict[str, Any]]:
        pass


class DatetimeFilterAtmotube(DatetimeFilter):


    def filter_packets(self, packets: List[Dict[str, Any]], sqltimestamp: str) -> List[Dict[str, Any]]:

        if sqltimestamp == EMPTY_STRING:
            return EMPTY_STRING

        filtered_packets = []
        if packets != EMPTY_LIST:
            for packet in packets:
                timestamp = DatetimeParser.atmotube_to_sqltimestamp(packet[ATMOTUBE_TIME_PARAM])
                if DatetimeParser.is_ts2_after_ts1(ts1 = sqltimestamp, ts2 = timestamp):
                    filtered_packets.append(packet)
        return filtered_packets


################################ DATETIME FILTER FACTORY ################################
class DatetimeFilterFactory(builtins.object):


    @classmethod
    def create_datetime_filter(cls, bot_personality: str) -> DatetimeFilter:

        if bot_personality == "atmotube":
            return DatetimeFilterAtmotube()
        else:
            raise SystemExit(f"{DatetimeFilterFactory.__name__}: invalid personality '{bot_personality}'.")
