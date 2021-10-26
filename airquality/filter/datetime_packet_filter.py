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


class DatetimePacketFilter(ABC):


    @abstractmethod
    def filter_packets(self, packets: Dict[str, Any], sqltimestamp: str) -> List[Dict[str, Any]]:
        pass


class DatetimePacketFilterAtmotube(DatetimePacketFilter):


    def filter_packets(self, packets: Dict[str, Any], sqltimestamp: str) -> List[Dict[str, Any]]:

        items = packets["data"]["items"]
        if sqltimestamp == EMPTY_STRING:
            return items

        filtered_packets = []
        if packets != EMPTY_LIST:
            for item in items:
                timestamp = DatetimeParser.atmotube_to_sqltimestamp(item[ATMOTUBE_TIME_PARAM])
                if DatetimeParser.is_ts2_after_ts1(ts1 = sqltimestamp, ts2 = timestamp):
                    filtered_packets.append(item)
        return filtered_packets


################################ DATETIME FILTER FACTORY ################################
class DatetimePacketFilterFactory(builtins.object):


    @classmethod
    def create_datetime_filter(cls, bot_personality: str) -> DatetimePacketFilter:

        if bot_personality == "atmotube":
            return DatetimePacketFilterAtmotube()
        else:
            raise SystemExit(f"{DatetimePacketFilterFactory.__name__}: cannot instantiate {DatetimePacketFilter.__name__} "
                             f"instance for personality='{bot_personality}'.")
