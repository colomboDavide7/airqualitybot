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
from airquality.app import EMPTY_LIST


class APIPacketFilter(ABC):


    @abstractmethod
    def filter_packet(self, packets: List[Dict[str, Any]], filter_list: List[Any]) -> List[Dict[str, Any]]:
        pass


class APIPacketFilterPurpleair(APIPacketFilter):

    def filter_packet(self, packets: List[Dict[str, Any]], filter_list: List[Any]) -> List[Dict[str, Any]]:

        if not filter_list:
            return packets

        filtered_packets = EMPTY_LIST
        if packets != EMPTY_LIST:
            for packet in packets:
                sensor_name = f'{packet["name"]} ({packet["sensor_index"]})'
                if sensor_name not in filter_list:
                    filtered_packets.append(packet)
        return filtered_packets


################################ FACTORY ################################
class APIPacketFilterFactory(builtins.object):


    @staticmethod
    def create_api_packet_filter(bot_personality: str) -> APIPacketFilter:
        if bot_personality == "purpleair":
            return APIPacketFilterPurpleair()
        else:
            raise SystemExit(f"{APIPacketFilterFactory.create_api_packet_filter.__name__}: "
                             f"invalid personality '{bot_personality}'.")
