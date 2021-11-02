#################################################
#
# @Author: davidecolombo
# @Date: ven, 22-10-2021, 11:47
# @Description: this script defines the classes for picking sensor's API packet values
#
#################################################
import builtins
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from airquality.bridge.bridge_object import BridgeObject
from airquality.packet.apiparam_packet import APIParamPacketPurpleair
from airquality.constants.shared_constants import EMPTY_LIST


class APIPacketPicker(ABC):
    """Abstract Base Class for selecting (picking) a set of parameters from the API packets."""

    @abstractmethod
    def pick_packet_params(self, packets: List[Dict[str, Any]], param2pick: List[str]) -> List[Dict[str, Any]]:
        pass


class APIPacketPickerPurpleair(APIPacketPicker):

    def pick_packet_params(self, packets: List[Dict[str, Any]], param2pick: List[str]) -> List[Dict[str, Any]]:
        """This method build a new packet list from the 'packets' argument by picking only the parameters contained
        in the 'param2pick' list.

        If 'packets' is equal to EMPTY_LIST, empty list is returned.
        If 'param2pick' is equal to EMPTY_LIST, no picking operation is applied to packets."""

        new_packets = []
        if packets == EMPTY_LIST:
            return new_packets

        if param2pick == EMPTY_LIST:
            return packets

        for packet in packets:
            keys = packet.keys()  # packet keys for checking param validity

            new_packet = {}  # new packet dictionary
            for param in param2pick:
                if param not in keys:  # checking param validity
                    raise SystemExit(f"{APIPacketPickerPurpleair.__name__}: cannot pick param '{param}' from packet.")
                else:
                    new_packet[param] = packet[param]

            new_packets.append(new_packet)  # append new packet
        return new_packets


################################ FACTORY ################################
class APIPacketPickerFactory(builtins.object):

    @classmethod
    def create_api_packet_picker(cls, bot_personality: str) -> APIPacketPicker:

        if bot_personality == "purpleair":
            return APIPacketPickerPurpleair()
        else:
            raise SystemExit(f"{APIPacketPickerFactory.__name__}: cannot instantiate {APIPacketPicker.__name__} "
                             f"instance for personality='{bot_personality}'.")
