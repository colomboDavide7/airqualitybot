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
from airquality.constants.shared_constants import EMPTY_LIST
from airquality.picker.api_packet_picker import APIPacketPicker


class APIPacketFilter(ABC):
    """Abstract Base Class that defines method for filtering a set of packets coming from the sensor's API."""

    @abstractmethod
    def filter_packet(self, packets: List[Dict[str, Any]], filter_list: List[Any]) -> List[Dict[str, Any]]:
        pass



class APIPacketFilterPurpleair(APIPacketFilter):


    def filter_packet(self, packets: List[Dict[str, Any]], filter_list: List[Any]) -> List[Dict[str, Any]]:
        """This method defines the rules for filtering purpleair API packets based on names.

        A valid purpleair name is of the form: 'sensor_name (sensor_index)'.

        If 'filter_list' argument is equal to 'EMPTY_LIST', this method returns the packets as they are passed.

        If 'packets' argument is equal to 'EMPTY_LIST' this method returns EMPTY_LIST value."""

        if filter_list == EMPTY_LIST:
            return packets

        filtered_packets = EMPTY_LIST
        if packets != EMPTY_LIST:
            for packet in packets:
                # f'{packet["name"]} ({packet["sensor_index"]})'
                sensor_name = APIPacketPicker.pick_sensor_name_from_identifier(packet = packet, identifier = "purpleair")
                if sensor_name not in filter_list:
                    filtered_packets.append(packet)
        return filtered_packets


################################ FACTORY ################################
class APIPacketFilterFactory(builtins.object):


    @staticmethod
    def create_api_packet_filter(bot_personality: str) -> APIPacketFilter:
        """Simple factory method for creating 'APIPacketFilter' instance from 'bot_personality'."""

        if bot_personality == "purpleair":
            return APIPacketFilterPurpleair()
