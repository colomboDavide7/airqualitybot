#################################################
#
# @Author: davidecolombo
# @Date: lun, 25-10-2021, 12:20
# @Description: this script defines the classes for filtering packets coming from sensor's API based on some criteria
#
#################################################
import builtins
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from airquality.constants.shared_constants import EMPTY_LIST, \
    PURPLEAIR_NAME_PARAM, PURPLEAIR_SENSOR_IDX_PARAM


class IdentifierPacketFilter(ABC):
    """Abstract Base Class that defines method for filtering a set of packets coming from the sensor's API."""


    @abstractmethod
    def filter_packets(self, packets: List[Dict[str, Any]], identifiers: List[str]) -> List[Dict[str, Any]]:
        pass


class IdentifierPacketFilterPurpleair(IdentifierPacketFilter):


    def filter_packets(self, packets: List[Dict[str, Any]], identifiers: List[str]) -> List[Dict[str, Any]]:

        if identifiers == EMPTY_LIST:
            return packets

        filtered_packets = []
        if packets != EMPTY_LIST:
            for packet in packets:
                sensor_name = f"{packet[PURPLEAIR_NAME_PARAM]} ({packet[PURPLEAIR_SENSOR_IDX_PARAM]})"
                if sensor_name not in identifiers:
                    filtered_packets.append(packet)
        return filtered_packets


################################ FACTORY ################################
class IdentifierPacketFilterFactory(builtins.object):


    @classmethod
    def create_identifier_filter(cls, bot_personality: str) -> IdentifierPacketFilter:

        if bot_personality == "purpleair":
            return IdentifierPacketFilterPurpleair()
        else:
            raise SystemExit(f"{IdentifierPacketFilterFactory.__name__}: cannot instantiate {IdentifierPacketFilter.__name__} "
                             f"instance for personality='{bot_personality}'.")
