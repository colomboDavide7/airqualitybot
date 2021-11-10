#################################################
#
# @Author: davidecolombo
# @Date: lun, 25-10-2021, 10:54
# @Description: this script defines the classes for dynamically reshaping packets from sensor's API
#
#################################################
import abc
from typing import Dict, Any, List

THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_1A = {"field1": "pm1.0_atm_a", "field2": "pm2.5_atm_a",
                                             "field3": "pm10.0_atm_a", "field6": "temperature_a",
                                             "field7": "humidity_a"}
THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_1B = {"field1": "pm1.0_atm_b", "field2": "pm2.5_atm_b",
                                             "field3": "pm10.0_atm_b", "field6": "pressure_b"}
THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_2A = {"field1": "0.3_um_count_a", "field2": "0.5_um_count_a",
                                             "field3": "1.0_um_count_a", "field4": "2.5_um_count_a",
                                             "field5": "5.0_um_count_a", "field6": "10.0_um_count_a"}
THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_2B = {"field1": "0.3_um_count_b", "field2": "0.5_um_count_b",
                                             "field3": "1.0_um_count_b", "field4": "2.5_um_count_b",
                                             "field5": "5.0_um_count_b", "field6": "10.0_um_count_b"}


################################ ABSTRACT BASE CLASS ################################
class PacketReshaper(abc.ABC):

    def __init__(self):
        self.channel_name = ""

    @property
    def ch_name(self):
        return self.channel_name

    @ch_name.setter
    def ch_name(self, value):
        self.channel_name = value

    @abc.abstractmethod
    def reshape(self, api_answer: Dict[str, Any]) -> List[Dict[str, Any]]:
        pass


################################ PURPLEAIR PACKET RESHAPER ################################
class PurpleairPacketReshaper(PacketReshaper):

    def reshape(self, api_answer: Dict[str, Any]) -> List[Dict[str, Any]]:
        fields = api_answer['fields']
        data = api_answer['data']
        reshaped_packets = []
        for d in data:
            reshaped_packets.append(dict(zip(fields, d)))
        return reshaped_packets


################################ THINGSPEAK PACKET RESHAPER ################################
class ThingspeakPacketReshaper(PacketReshaper):

    def reshape(self, api_answer: Dict[str, Any]) -> List[Dict[str, Any]]:
        if self.channel_name == '1A':
            field_to_use = THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_1A
        elif self.channel_name == '1B':
            field_to_use = THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_1B
        elif self.channel_name == '2A':
            field_to_use = THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_2A
        elif self.channel_name == '2B':
            field_to_use = THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_2B
        else:
            raise SystemExit(f"{ThingspeakPacketReshaper.__name__} bad parameters => channel_name='{self.channel_name}'")

        reshaped_packets = []
        for feed in api_answer['feeds']:
            reshaped_packet = {'created_at': feed['created_at'], 'fields': []}
            for field in field_to_use.keys():
                reshaped_packet['fields'].append({'name': field_to_use[field], 'value': feed[field]})
            reshaped_packets.append(reshaped_packet)
        return reshaped_packets


################################ ATMOTUBE PACKET RESHAPER ################################

class AtmotubePacketReshaper(PacketReshaper):

    def reshape(self, api_answer: Dict[str, Any]) -> List[Dict[str, Any]]:
        return api_answer['data']['items']
