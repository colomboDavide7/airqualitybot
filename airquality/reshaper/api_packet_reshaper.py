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
from airquality.parser.datetime_parser import DatetimeParser
from airquality.packet.apiparam_single_packet import APIParamSinglePacket, APIParamSinglePacketPurpleair
from airquality.constants.shared_constants import EMPTY_LIST, EMPTY_DICT, \
    PURPLEAIR_DATA_PARAM, PURPLEAIR_FIELDS_PARAM, THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_1A, \
    THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_1B, THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_2A, \
    THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_2B

# ThingSpeak APIPacketReshaper constants for reshaping API packets
from airquality.constants.shared_constants import THINGSPEAK_API_RESHAPER_TIME

# ThingSpeak API packet decoding constants for decoding an API packet
from airquality.constants.shared_constants import THINGSPEAK_API_DECODE_FEEDS, THINGSPEAK_API_DECODE_CHANNEL, \
    THINGSPEAK_API_DECODE_NAME, THINGSPEAK_API_DECODE_CREATED_AT, THINGSPEAK_CHANNEL_DECODE, THINGSPEAK_COUNTERS_DECODE


class APIPacketReshaper(ABC):

    @abstractmethod
    def reshape_packet(self, api_answer: Dict[str, Any]) -> List[APIParamSinglePacket]:
        pass


class APIPacketReshaperPurpleair(APIPacketReshaper):

    def reshape_packet(self, api_answer: Dict[str, Any]) -> List[APIParamSinglePacketPurpleair]:
        """This method takes a purpleair API answer and reshape it by creating a dictionary association between the
        'fields' parameter and the 'data' parameter for each item in the 'data' list."""

        fields = api_answer[PURPLEAIR_FIELDS_PARAM]
        n_fields = len(fields)

        reshaped_packets = []
        if api_answer[PURPLEAIR_DATA_PARAM] != EMPTY_LIST:
            for data in api_answer[PURPLEAIR_DATA_PARAM]:
                rpacket = {}
                for i in range(n_fields):
                    key = fields[i]
                    val = data[i]
                    rpacket[key] = val
                reshaped_packets.append(APIParamSinglePacketPurpleair(api_param=rpacket))
        return reshaped_packets


################################ THINGSPEAK API PACKET RESHAPER ################################

class APIPacketReshaperThingspeak(APIPacketReshaper):

    def reshape_packet(self, api_answer: Dict[str, Any]) -> List[Dict[str, Any]]:

        if api_answer == EMPTY_DICT:
            raise SystemExit(f"{APIPacketReshaperThingspeak.__name__}: cannot reshaper api answer when is empty.")

        channel = api_answer[THINGSPEAK_API_DECODE_CHANNEL]
        field_to_use = THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_1A
        sensor_name = channel[THINGSPEAK_API_DECODE_NAME]

        # SELECT THE RESHAPE MAPPING BASED ON PRIMARY/SECONDARY DATA AND CHANNEL A/B
        if THINGSPEAK_CHANNEL_DECODE in sensor_name:
            if THINGSPEAK_COUNTERS_DECODE in sensor_name:
                field_to_use = THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_2B
            else:
                field_to_use = THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_1B
        else:
            if THINGSPEAK_COUNTERS_DECODE in sensor_name:
                field_to_use = THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_2A

        # Decode the "fieldN" value in the 'api_answer' header with the chosen mapping (field_to_use)
        selected_fields = {}
        for param in channel.keys():
            if channel[param] in field_to_use.keys():
                selected_fields[param] = field_to_use[channel[param]]

        reshaped_packets = []
        feeds = api_answer[THINGSPEAK_API_DECODE_FEEDS]
        for feed in feeds:
            reshaped_packet = {}
            timestamp = DatetimeParser.thingspeak_to_sqltimestamp(ts=feed[THINGSPEAK_API_DECODE_CREATED_AT])
            reshaped_packet[THINGSPEAK_API_RESHAPER_TIME] = timestamp
            for field in feed.keys():
                if field in selected_fields.keys():
                    reshaped_packet[selected_fields[field]] = feed[field]
            reshaped_packets.append(reshaped_packet)
        return reshaped_packets


################################ FACTORY ################################
class APIPacketReshaperFactory(builtins.object):

    @classmethod
    def create_api_packet_reshaper(cls, bot_personality: str) -> APIPacketReshaper:
        if bot_personality == "purpleair":
            return APIPacketReshaperPurpleair()
        elif bot_personality == "thingspeak":
            return APIPacketReshaperThingspeak()
        else:
            raise SystemExit(f"{APIPacketReshaperFactory.__name__}: cannot instantiate {APIPacketReshaper.__name__} "
                             f"instance for personality='{bot_personality}'.")
