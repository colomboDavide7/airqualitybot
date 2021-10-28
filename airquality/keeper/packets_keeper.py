#################################################
#
# @Author: davidecolombo
# @Date: gio, 28-10-2021, 15:17
# @Description: this script defines the classes that only keeps the API packets that match a given condition
#
#################################################
import builtins
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from airquality.constants.shared_constants import EMPTY_LIST, PURPLEAIR_SENSOR_IDX_PARAM, PURPLEAIR_NAME_PARAM


class APIPacketKeeper(ABC):


    @abstractmethod
    def keep_packets(self, packets: List[Dict[str, Any]], identifiers: List[str]) -> List[Dict[str, Any]]:
        pass


class APIPacketKeeperPurpleair(APIPacketKeeper):


    def keep_packets(self, packets: List[Dict[str, Any]], identifiers: List[str]) -> List[Dict[str, Any]]:

        if packets == EMPTY_LIST:
            return []

        if identifiers == EMPTY_LIST:
            return packets


        new_packets = []
        for packet in packets:
            sensor_name = f"{packet[PURPLEAIR_NAME_PARAM]} ({packet[PURPLEAIR_SENSOR_IDX_PARAM]})"
            if sensor_name in identifiers:
                new_packets.append(packet)
        return new_packets






################################ FACTORY ################################
class APIPacketKeeperFactory(builtins.object):


    @classmethod
    def create_packet_keeper(cls, bot_personality: str) -> APIPacketKeeper:

        if bot_personality == "purpleair":
            return APIPacketKeeperPurpleair()
        else:
            raise SystemExit(f"{APIPacketKeeperFactory.__name__}: cannot instantiate {APIPacketKeeper.__name__} "
                             f"instance for personality='{bot_personality}'.")
