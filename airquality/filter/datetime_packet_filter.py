#################################################
#
# @Author: davidecolombo
# @Date: mar, 26-10-2021, 12:52
# @Description: this script defines the classes for filtering packets by acquisition time
#
#################################################
from typing import List
from airquality.parser.datetime_parser import DatetimeParser
from airquality.constants.shared_constants import EMPTY_STRING


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
