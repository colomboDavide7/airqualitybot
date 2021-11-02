#################################################
#
# @Author: davidecolombo
# @Date: lun, 25-10-2021, 12:20
# @Description: this script defines the classes for filtering packets coming from sensor's API based on some criteria
#
#################################################
import builtins
from abc import ABC, abstractmethod
from typing import List
from airquality.packet.plain_api_packet import PlainAPIPacketPurpleair, PlainAPIPacket
from airquality.constants.shared_constants import EMPTY_LIST


class IdentifierPacketFilter(ABC):
    """Abstract Base Class that defines an abstract method for filtering API answer packets based on a sensor identifier.

    This can be useful to check whether a given sensor is already present in the database or not."""

    @abstractmethod
    def filter_packets(self, packets: List[PlainAPIPacket], identifiers: List[str]) -> List[PlainAPIPacket]:
        pass


class IdentifierPacketFilterPurpleair(IdentifierPacketFilter):

    def filter_packets(self, packets: List[PlainAPIPacketPurpleair], identifiers: List[str]
                       ) -> List[PlainAPIPacketPurpleair]:
        """This method filters the purpleair packets based on 'sensor_name' that is computed dynamically inside the method.

        The 'identifiers' argument is a list of purpleair 'sensor_name'(s)."""

        if identifiers == EMPTY_LIST:
            return packets

        filtered_packets = []
        if packets != EMPTY_LIST:
            for packet in packets:
                if packet.purpleair_identifier not in identifiers:
                    filtered_packets.append(packet)
        return filtered_packets


################################ FACTORY ################################
class IdentifierPacketFilterFactory(builtins.object):

    @classmethod
    def create_identifier_filter(cls, bot_personality: str) -> IdentifierPacketFilter:

        if bot_personality == "purpleair":
            return IdentifierPacketFilterPurpleair()
        else:
            raise SystemExit(
                f"{IdentifierPacketFilterFactory.__name__}: cannot instantiate {IdentifierPacketFilter.__name__} "
                f"instance for personality='{bot_personality}'.")
