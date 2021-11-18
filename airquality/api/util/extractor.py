#################################################
#
# Author: Davide Colombo
# @Date: lun, 25-10-2021, 10:54
# @Description: this script defines the classes for dynamically reshaping packets from sensor's API
#
#################################################
import abc
from typing import Dict, Any, List
import airquality.api.config as c


def get_data_extractor(sensor_type: str):

    if sensor_type == 'purpleair':
        return PurpleairDataExtractor()
    elif sensor_type == 'atmotube':
        return AtmotubeDataExtractor()
    elif sensor_type == 'thingspeak':
        return ThingspeakDataExtractor()
    else:
        raise SystemExit(f"'{get_data_extractor.__name__}():' bad type '{sensor_type}'")


################################ ABSTRACT BASE CLASS ################################
class DataExtractor(abc.ABC):

    @abc.abstractmethod
    def extract(self, parsed_response: Dict[str, Any], channel_name="") -> List[Dict[str, Any]]:
        pass


################################ PURPLEAIR DATA EXTRACTOR ################################
class PurpleairDataExtractor(DataExtractor):

    def extract(self, parsed_response: Dict[str, Any], channel_name="") -> List[Dict[str, Any]]:
        data_packets = []
        for data_packet in parsed_response['data']:
            data_packets.append(dict(zip(parsed_response['fields'], data_packet)))
        return data_packets


################################ THINGSPEAK DATA EXTRACTOR ################################
class ThingspeakDataExtractor(DataExtractor):

    def extract(self, parsed_response: Dict[str, Any], channel_name="") -> List[Dict[str, Any]]:

        if channel_name == '1A':
            field_to_use = c.THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_1A
        elif channel_name == '1B':
            field_to_use = c.THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_1B
        elif channel_name == '2A':
            field_to_use = c.THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_2A
        elif channel_name == '2B':
            field_to_use = c.THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_2B
        else:
            raise SystemExit(f"{ThingspeakDataExtractor.__name__}: bad parameter => invalid channel_name='{channel_name}'")

        data_packets = []
        for feed in parsed_response['feeds']:
            data_packet = {'created_at': feed['created_at'], c.FIELDS: []}
            for field in field_to_use.keys():
                data_packet[c.FIELDS].append({c.FIELD_NAME: field_to_use[field], c.FIELD_VALUE: feed[field]})
            data_packets.append(data_packet)
        return data_packets


################################ ATMOTUBE DATA EXTRACTOR ################################

class AtmotubeDataExtractor(DataExtractor):

    def extract(self, parsed_response: Dict[str, Any], channel_name="") -> List[Dict[str, Any]]:
        return parsed_response['data']['items']
