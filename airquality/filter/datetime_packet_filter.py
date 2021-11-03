#################################################
#
# @Author: davidecolombo
# @Date: mar, 26-10-2021, 12:52
# @Description: this script defines the classes for filtering packets by acquisition time
#
#################################################
import builtins
from abc import ABC, abstractmethod
from typing import List
from airquality.parser.datetime_parser import DatetimeParser
from airquality.plain.plain_api_packet import PlainAPIPacket, PlainAPIPacketAtmotube
from airquality.constants.shared_constants import EMPTY_STRING


class DatetimePacketFilter(ABC):
    """Abstract Base Class for datetime filter instances. The purpose of this set of classes is to filter out all
    the packets downloaded from the API that are acquired before a given filter timestamp."""

    @abstractmethod
    def filter_packets(self, packets: List[PlainAPIPacket], sqltimestamp: str) -> List[PlainAPIPacket]:
        pass


class DatetimePacketFilterAtmotube(DatetimePacketFilter):

    def filter_packets(self, packets: List[PlainAPIPacketAtmotube], sqltimestamp: str) -> List[PlainAPIPacketAtmotube]:

        if not packets:
            return []

        if sqltimestamp == EMPTY_STRING:
            return packets

        filtered_packets = []
        for packet in packets:
            if DatetimeParser.is_ts2_after_ts1(ts1=sqltimestamp, ts2=packet.time):
                filtered_packets.append(packet)
        return filtered_packets


################################ DATETIME FILTER FACTORY ################################
class DatetimePacketFilterFactory(builtins.object):

    @classmethod
    def create_datetime_filter(cls, bot_personality: str) -> DatetimePacketFilter:

        if bot_personality == "atmotube":
            return DatetimePacketFilterAtmotube()
        else:
            raise SystemExit(
                f"{DatetimePacketFilterFactory.__name__}: cannot instantiate {DatetimePacketFilter.__name__} "
                f"instance for personality='{bot_personality}'.")
