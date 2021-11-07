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
from airquality.plain.plain_api_packet_mergeable import PlainAPIPacketThingspeakPrimaryChannelAFactory, \
    PlainAPIPacketThingspeakPrimaryChannelBFactory, PlainAPIPacketThingspeakSecondaryChannelAFactory, \
    PlainAPIPacketThingspeakSecondaryChannelBFactory, PlainAPIPacketMergeable

from airquality.constants.shared_constants import EMPTY_LIST, \
    PURPLEAIR_DATA_PARAM, PURPLEAIR_FIELDS_PARAM, THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_1A, \
    THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_1B, THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_2A, \
    THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_2B

# ThingSpeak API sqlwrapper decoding constants for decoding an API sqlwrapper
from airquality.constants.shared_constants import THINGSPEAK_API_DECODE_FEEDS, THINGSPEAK_API_DECODE_CHANNEL, \
    THINGSPEAK_API_DECODE_NAME, THINGSPEAK_CHANNEL_DECODE_SYMBOL, THINGSPEAK_COUNTERS_DECODE_SYMBOL


class APIPacketReshaper(ABC):

    @abstractmethod
    def reshape_packet(self, api_answer: Dict[str, Any]) -> List[Dict[str, Any]]:
        pass


class APIPacketReshaperPurpleair(APIPacketReshaper):

    def reshape_packet(self, api_answer: Dict[str, Any]) -> List[Dict[str, Any]]:
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
                reshaped_packets.append(rpacket)
        return reshaped_packets


################################ THINGSPEAK API PACKET RESHAPER ################################

class APIPacketReshaperThingspeak(APIPacketReshaper):

    def reshape_packet(self, api_answer: Dict[str, Any]) -> List[PlainAPIPacketMergeable]:

        feeds = api_answer[THINGSPEAK_API_DECODE_FEEDS]
        if not feeds:
            return []

        channel = api_answer[THINGSPEAK_API_DECODE_CHANNEL]
        sensor_name = channel[THINGSPEAK_API_DECODE_NAME]

        field_to_use = THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_1A
        factory = PlainAPIPacketThingspeakPrimaryChannelAFactory()

        # SELECT THE RESHAPE MAPPING BASED ON PRIMARY/SECONDARY DATA AND CHANNEL A/B
        if THINGSPEAK_CHANNEL_DECODE_SYMBOL in sensor_name:
            if THINGSPEAK_COUNTERS_DECODE_SYMBOL in sensor_name:
                field_to_use = THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_2B
                factory = PlainAPIPacketThingspeakSecondaryChannelBFactory()
            else:
                field_to_use = THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_1B
                factory = PlainAPIPacketThingspeakPrimaryChannelBFactory()
        else:
            if THINGSPEAK_COUNTERS_DECODE_SYMBOL in sensor_name:
                field_to_use = THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_2A
                factory = PlainAPIPacketThingspeakSecondaryChannelAFactory()

        # Decode the "fieldN" value in the 'api_answer' header with the chosen mapping (field_to_use)
        selected_fields = {}
        for param in channel.keys():
            if channel[param] in field_to_use.keys():
                selected_fields[param] = field_to_use[channel[param]]

        reshaped_packets = []
        for feed in feeds:
            reshaped_packet = {'created_at': feed['created_at']}
            for field in feed.keys():
                if field in selected_fields.keys():
                    reshaped_packet[selected_fields[field]] = feed[field]
            reshaped_packets.append(factory.make_plain_object(api_answer=reshaped_packet))
        return reshaped_packets


################################ ATMOTUBE API PACKET RESHAPER ################################

class APIPacketReshaperAtmotube(APIPacketReshaper):

    def reshape_packet(self, api_answer: Dict[str, Any]) -> List[Dict[str, Any]]:

        items = api_answer['data']['items']
        if not items:
            return []

        reshaped_items = []
        for item in items:
            reshaped_items.append(item)
        return reshaped_items


################################ FACTORY ################################
class APIPacketReshaperFactory(builtins.object):

    @classmethod
    def create_api_packet_reshaper(cls, bot_personality: str) -> APIPacketReshaper:
        if bot_personality == "purpleair":
            return APIPacketReshaperPurpleair()
        elif bot_personality == "thingspeak":
            return APIPacketReshaperThingspeak()
        elif bot_personality == 'atmotube':
            return APIPacketReshaperAtmotube()
        else:
            raise SystemExit(f"{APIPacketReshaperFactory.__name__}: cannot instantiate {APIPacketReshaper.__name__} "
                             f"instance for personality='{bot_personality}'.")
