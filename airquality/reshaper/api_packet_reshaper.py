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
from airquality.constants.shared_constants import EMPTY_LIST, \
    PURPLEAIR_DATA_PARAM, PURPLEAIR_FIELDS_PARAM


class APIPacketReshaper(ABC):


    @abstractmethod
    def reshape_packet(self, api_answer: Dict[str, Any]) -> List[Dict[str, Any]]:
        pass


class APIPacketReshaperPurpleair(APIPacketReshaper):


    def reshape_packet(self, api_answer: Dict[str, Any]) -> List[Dict[str, Any]]:
        """This method takes a purpleair API answer and reshape it by creating a dictionary association between the
        'fields' parameter and the 'data' parameter for each item in the 'data' list."""

        reshaped_packets = []
        fields = api_answer[PURPLEAIR_FIELDS_PARAM]
        n_fields = len(fields)

        if api_answer[PURPLEAIR_DATA_PARAM] != EMPTY_LIST:
            for data in api_answer[PURPLEAIR_DATA_PARAM]:
                rpacket = {}
                for i in range(n_fields):
                    key = fields[i]
                    val = data[i]
                    rpacket[key] = val
                reshaped_packets.append(rpacket)
        return reshaped_packets


################################ FACTORY ################################
class APIPacketReshaperFactory(builtins.object):

    @classmethod
    def create_api_packet_reshaper(cls, bot_personality: str) -> APIPacketReshaper:
        if bot_personality == "purpleair":
            return APIPacketReshaperPurpleair()
        else:
            raise SystemExit(f"{APIPacketReshaperFactory.__name__}: don't recognized personality '{bot_personality}'.")
