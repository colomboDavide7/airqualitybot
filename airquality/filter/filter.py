#################################################
#
# @Author: davidecolombo
# @Date: lun, 25-10-2021, 12:20
# @Description: this script defines the classes for filtering packets coming from sensor's API based on some criteria
#
#################################################
import builtins
from typing import Dict, Any, List
from airquality.picker.api_packet_picker import APIPacketPicker
from airquality.parser.datetime_parser import DatetimeParser
from airquality.constants.shared_constants import EMPTY_LIST, EMPTY_STRING


class APIPacketFilter(builtins.object):
    """Abstract Base Class that defines method for filtering a set of packets coming from the sensor's API."""

    @classmethod
    def filter_packet_by_sensor_name(cls, packets: List[Dict[str, Any]], filter_name_list: List[Any], identifier: str
                                     ) -> List[Dict[str, Any]]:

        if filter_name_list == EMPTY_LIST:
            return packets

        filtered_packets = EMPTY_LIST
        if packets != EMPTY_LIST:
            for packet in packets:
                sensor_name = APIPacketPicker.pick_sensor_name_from_identifier(packet = packet, identifier = identifier)
                if sensor_name not in filter_name_list:
                    filtered_packets.append(packet)
        return filtered_packets


    @classmethod
    def filter_packet_from_timestamp_on(cls, packets: List[Dict[str, Any]], sqltimestamp: str, identifier: str
                                        ) -> List[Dict[str, Any]]:

        if sqltimestamp == EMPTY_STRING:
            return EMPTY_STRING

        filtered_packets = EMPTY_LIST
        if packets != EMPTY_LIST:
            for packet in packets:
                timestamp = APIPacketPicker.pick_packet_timestamp_from_identifier(packet = packet, identifier = identifier)
                if DatetimeParser.is_ts2_after_ts1(ts1 = sqltimestamp, ts2 = timestamp):
                    filtered_packets.append(packet)
        return filtered_packets
