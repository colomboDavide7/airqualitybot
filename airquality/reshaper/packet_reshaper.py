#################################################
#
# @Author: davidecolombo
# @Date: lun, 25-10-2021, 10:54
# @Description: this script defines the classes for dynamically reshaping packets from sensor's API
#
#################################################
from abc import ABC, abstractmethod
from typing import Dict, Any, List

from airquality.constants.shared_constants import  THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_1A, \
    THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_1B, THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_2A, \
    THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_2B


################################ ABSTRACT BASE CLASS ################################
class PacketReshaper(ABC):

    @abstractmethod
    def reshape_packet(self, api_answer: Dict[str, Any]) -> List[Dict[str, Any]]:
        pass


################################ PURPLEAIR PACKET RESHAPER ################################
class PurpleairPacketReshaper(PacketReshaper):

    def reshape_packet(self, api_answer: Dict[str, Any]) -> List[Dict[str, Any]]:
        """This method takes a purpleair API answer and reshape it by creating a dictionary association between the
        'fields' parameter and the 'data' parameter for each item in the 'data' list."""

        fields = api_answer['fields']
        n_fields = len(fields)

        reshaped_packets = []
        if api_answer['data']:
            for data in api_answer['data']:
                rpacket = {}
                for i in range(n_fields):
                    key = fields[i]
                    val = data[i]
                    rpacket[key] = val
                reshaped_packets.append(rpacket)
        return reshaped_packets


################################ THINGSPEAK PACKET RESHAPER ################################
class ThingspeakPacketReshaper(PacketReshaper):

    def reshape_packet(self, api_answer: Dict[str, Any]) -> List[Dict[str, Any]]:

        feeds = api_answer['feeds']
        if not feeds:
            return []

        channel = api_answer['channel']
        sensor_name = channel['name']
        field_to_use = THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_1A

        # SELECT THE RESHAPE MAPPING BASED ON PRIMARY/SECONDARY DATA AND CHANNEL A/B
        if '_b' in sensor_name:
            if 'Counters' in sensor_name:
                field_to_use = THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_2B
            else:
                field_to_use = THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_1B
        else:
            if 'Counters' in sensor_name:
                field_to_use = THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_2A

        # Decode the "fieldN" value in the 'api_answer' header with the chosen mapping (field_to_use)
        selected_fields = {}
        for param in channel.keys():
            if channel[param] in field_to_use.keys():
                selected_fields[param] = field_to_use[channel[param]]

        reshaped_packets = []
        for feed in feeds:
            reshaped_packet = {'created_at': feed['created_at'], 'fields': []}
            for field in feed.keys():
                if field in selected_fields.keys():
                    reshaped_packet['fields'].append({'name': selected_fields[field], 'value': feed[field]})
            reshaped_packets.append(reshaped_packet)
        return reshaped_packets


################################ ATMOTUBE PACKET RESHAPER ################################

class AtmotubePacketReshaper(PacketReshaper):

    def reshape_packet(self, api_answer: Dict[str, Any]) -> List[Dict[str, Any]]:

        items = api_answer['data']['items']
        if not items:
            return []

        reshaped_items = []
        for item in items:
            reshaped_items.append(item)
        return reshaped_items

# ################################ FACTORY ################################
# class PacketReshaperFactory(object):
#
#     def __init__(self, reshaper_class=PacketReshaper):
#         self.reshaper_class = reshaper_class
#
#     def make_reshaper(self) -> PacketReshaper:
#         return self.reshaper_class()
