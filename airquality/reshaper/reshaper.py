#################################################
#
# @Author: davidecolombo
# @Date: lun, 25-10-2021, 10:54
# @Description: this script defines the classes for dynamically reshaping packets from sensor's API
#
#################################################
import builtins
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from airquality.app import EMPTY_LIST


class APIPacketReshaper(ABC):


    @abstractmethod
    def reshape_packet(self, parsed_api_answer: Dict[str, Any]) -> List[Dict[str, Any]]:
        pass


class APIPacketReshaperPurpleair(APIPacketReshaper):

    def reshape_packet(self, parsed_api_answer: Dict[str, Any]) -> List[Dict[str, Any]]:
        reshaped_packets = []
        n_fields = len(parsed_api_answer["fields"])

        if parsed_api_answer["data"] != EMPTY_LIST:
            for data in parsed_api_answer["data"]:
                packet = {}
                for i in range(n_fields):
                    key = parsed_api_answer["fields"][i]
                    val = data[i]
                    packet[key] = val

                reshaped_packets.append(packet)

        return reshaped_packets

################################ FACTORY ################################
class APIPacketReshaperFactory(builtins.object):

    @staticmethod
    def create_api_packet_reshaper(bot_personality: str) -> APIPacketReshaper:
        if bot_personality == "purpleair":
            return APIPacketReshaperPurpleair()
        else:
            raise SystemExit(f"{APIPacketReshaperFactory.create_api_packet_reshaper.__name__}: "
                             f"invalid bot personality '{bot_personality}'.")
