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
import airquality.adapter.config as adapt_const


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

    @abc.abstractmethod
    def _exit_on_bad_parsed_response(self, parsed_response: Dict[str, Any]):
        pass


################################ PURPLEAIR DATA EXTRACTOR ################################
class PurpleairDataExtractor(DataExtractor):

    def extract(self, parsed_response: Dict[str, Any], channel_name="") -> List[Dict[str, Any]]:
        self._exit_on_bad_parsed_response(parsed_response=parsed_response)

        data_packets = []
        for data_packet in parsed_response['data']:
            data_packets.append(dict(zip(parsed_response['fields'], data_packet)))
        return data_packets

    def _exit_on_bad_parsed_response(self, parsed_response: Dict[str, Any]):
        if 'data' not in parsed_response:
            raise SystemExit(f"{PurpleairDataExtractor.__name__}: bad api response: missing 'data' item")
        if 'fields' not in parsed_response:
            raise SystemExit(f"{PurpleairDataExtractor.__name__}: bad api response: missing 'fields' item")


################################ THINGSPEAK DATA EXTRACTOR ################################
class ThingspeakDataExtractor(DataExtractor):

    def extract(self, parsed_response: Dict[str, Any], channel_name="") -> List[Dict[str, Any]]:

        if channel_name == adapt_const.FST_CH_A:
            field_to_use = c.THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_1A
        elif channel_name == adapt_const.FST_CH_B:
            field_to_use = c.THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_1B
        elif channel_name == adapt_const.SND_CH_A:
            field_to_use = c.THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_2A
        elif channel_name == adapt_const.SND_CH_B:
            field_to_use = c.THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_2B
        else:
            raise SystemExit(f"{ThingspeakDataExtractor.__name__}: bad parameter => invalid channel_name='{channel_name}'")

        # Check parsed response correct shape
        if 'feeds' not in parsed_response:
            raise SystemExit(f"{ThingspeakDataExtractor.__name__}: bad api response: missing 'feeds' item")

        data_packets = []
        for feed in parsed_response['feeds']:
            self._exit_on_bad_parsed_response(feed)
            data_packet = {'created_at': feed['created_at'], c.FIELDS: []}
            for field in field_to_use.keys():
                data_packet[c.FIELDS].append({c.FIELD_NAME: field_to_use[field], c.FIELD_VALUE: feed[field]})
            data_packets.append(data_packet)
        return data_packets

    def _exit_on_bad_parsed_response(self, parsed_response: Dict[str, Any]):
        if 'created_at' not in parsed_response:
            raise SystemExit(f"{ThingspeakDataExtractor.__name__}: bad api response: missing 'created_at' item")


################################ ATMOTUBE DATA EXTRACTOR ################################

class AtmotubeDataExtractor(DataExtractor):

    def extract(self, parsed_response: Dict[str, Any], channel_name="") -> List[Dict[str, Any]]:
        self._exit_on_bad_parsed_response(parsed_response=parsed_response)
        return parsed_response['data']['items']

    def _exit_on_bad_parsed_response(self, parsed_response: Dict[str, Any]):
        if 'data' not in parsed_response:
            raise SystemExit(f"{AtmotubeDataExtractor.__name__}: bad api response: missing 'data' item")
        if 'items' not in parsed_response['data']:
            raise SystemExit(f"{AtmotubeDataExtractor.__name__}: bad api response: 'data' item miss 'items' list.")
