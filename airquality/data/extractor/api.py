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


def get_api_extractor_class(sensor_type: str):

    if sensor_type == 'purpleair':
        return PurpleairAPIExtractor
    elif sensor_type == 'atmotube':
        return AtmotubeAPIExtractor
    elif sensor_type == 'thingspeak':
        return ThingspeakAPIExtractor


################################ ABSTRACT BASE CLASS ################################
class APIExtractor(abc.ABC):

    def __init__(self, api_answer: Dict[str, Any], channel_name=""):
        self.channel_name = channel_name
        self.api_answer = api_answer

    @abc.abstractmethod
    def extract(self) -> List[Dict[str, Any]]:
        pass


################################ PURPLEAIR PACKET RESHAPER ################################
class PurpleairAPIExtractor(APIExtractor):

    def __init__(self, api_answer: Dict[str, Any], channel_name=""):
        super(PurpleairAPIExtractor, self).__init__(api_answer=api_answer, channel_name=channel_name)

    def extract(self) -> List[Dict[str, Any]]:
        data_packets = []
        for data_packet in self.api_answer['data']:
            data_packets.append(dict(zip(self.api_answer['fields'], data_packet)))
        return data_packets


################################ THINGSPEAK PACKET RESHAPER ################################
class ThingspeakAPIExtractor(APIExtractor):

    def __init__(self, api_answer: Dict[str, Any], channel_name=""):
        super(ThingspeakAPIExtractor, self).__init__(api_answer=api_answer, channel_name=channel_name)
        if self.channel_name == '1A':
            self.field_to_use = THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_1A
        elif self.channel_name == '1B':
            self.field_to_use = THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_1B
        elif self.channel_name == '2A':
            self.field_to_use = THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_2A
        elif self.channel_name == '2B':
            self.field_to_use = THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_2B
        else:
            raise SystemExit(f"{ThingspeakAPIExtractor.__name__} bad parameters => channel_name='{self.channel_name}'")

    def extract(self) -> List[Dict[str, Any]]:
        data_packets = []
        for feed in self.api_answer['feeds']:
            data_packet = {'created_at': feed['created_at'], 'fields': []}
            for field in self.field_to_use.keys():
                data_packet['fields'].append({'name': self.field_to_use[field], 'value': feed[field]})
            data_packets.append(data_packet)
        return data_packets


################################ ATMOTUBE PACKET RESHAPER ################################

class AtmotubeAPIExtractor(APIExtractor):

    def __init__(self, api_answer: Dict[str, Any], channel_name=""):
        super(AtmotubeAPIExtractor, self).__init__(api_answer=api_answer, channel_name=channel_name)

    def extract(self) -> List[Dict[str, Any]]:
        return self.api_answer['data']['items']
