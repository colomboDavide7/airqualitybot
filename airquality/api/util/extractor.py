#################################################
#
# Author: Davide Colombo
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


def get_data_extractor(sensor_type: str):

    if sensor_type == 'purpleair':
        return PurpleairDataExtractor()
    elif sensor_type == 'atmotube':
        return AtmotubeDataExtractor()
    elif sensor_type == 'thingspeak':
        return ThingspeakDataExtractor()


################################ ABSTRACT BASE CLASS ################################
class DataExtractor(abc.ABC):

    @abc.abstractmethod
    def extract(self, parsed_response: Dict[str, Any], channel_name="") -> List[Dict[str, Any]]:
        pass


################################ PURPLEAIR PACKET RESHAPER ################################
class PurpleairDataExtractor(DataExtractor):

    def extract(self, parsed_response: Dict[str, Any], channel_name="") -> List[Dict[str, Any]]:
        data_packets = []
        for data_packet in parsed_response['data']:
            data_packets.append(dict(zip(parsed_response['fields'], data_packet)))
        return data_packets


################################ THINGSPEAK PACKET RESHAPER ################################
class ThingspeakDataExtractor(DataExtractor):

    def extract(self, parsed_response: Dict[str, Any], channel_name="") -> List[Dict[str, Any]]:

        if channel_name == '1A':
            field_to_use = THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_1A
        elif channel_name == '1B':
            field_to_use = THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_1B
        elif channel_name == '2A':
            field_to_use = THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_2A
        elif channel_name == '2B':
            field_to_use = THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_2B
        else:
            raise SystemExit(f"{ThingspeakDataExtractor.__name__}: bad parameter => invalid channel_name='{channel_name}'")

        data_packets = []
        for feed in parsed_response['feeds']:
            data_packet = {'created_at': feed['created_at'], 'fields': []}
            for field in field_to_use.keys():
                data_packet['fields'].append({'name': field_to_use[field], 'value': feed[field]})
            data_packets.append(data_packet)
        return data_packets


################################ ATMOTUBE PACKET RESHAPER ################################

class AtmotubeDataExtractor(DataExtractor):

    def extract(self, parsed_response: Dict[str, Any], channel_name="") -> List[Dict[str, Any]]:
        return parsed_response['data']['items']
