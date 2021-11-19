#################################################
#
# Author: Davide Colombo
# @Date: lun, 25-10-2021, 10:54
# @Description: this script defines the classes for dynamically reshaping packets from sensor's API
#
#################################################
import abc
from typing import Dict, Any, List
import airquality.api.config as api_const
import airquality.adapter.config as adapt_const
import airquality.logger.loggable as log
import airquality.logger.util.decorator as log_decorator


def get_data_extractor(sensor_type: str, log_filename="app"):

    if sensor_type == 'purpleair':
        return PurpleairDataExtractor(log_filename=log_filename)
    elif sensor_type == 'atmotube':
        return AtmotubeDataExtractor(log_filename=log_filename)
    elif sensor_type == 'thingspeak':
        return ThingspeakDataExtractor(log_filename=log_filename)
    else:
        raise SystemExit(f"'{get_data_extractor.__name__}():' bad type '{sensor_type}'")


################################ ABSTRACT BASE CLASS ################################
class DataExtractor(log.Loggable):

    def __init__(self, log_filename="app"):
        super(DataExtractor, self).__init__(log_filename=log_filename)

    @abc.abstractmethod
    def extract(self, parsed_response: Dict[str, Any], channel_name="") -> List[Dict[str, Any]]:
        pass

    @abc.abstractmethod
    def _exit_on_bad_parsed_response(self, parsed_response: Dict[str, Any]):
        pass


################################ PURPLEAIR DATA EXTRACTOR ################################
class PurpleairDataExtractor(DataExtractor):

    def __init__(self, log_filename="app"):
        super(PurpleairDataExtractor, self).__init__(log_filename=log_filename)

    @log_decorator.log_decorator()
    def extract(self, parsed_response: Dict[str, Any], channel_name="") -> List[Dict[str, Any]]:

        self.log_info(f"{PurpleairDataExtractor.__name__}: try to extract API sensor data...")
        self._exit_on_bad_parsed_response(parsed_response=parsed_response)

        data_packets = []
        for data_packet in parsed_response['data']:
            data_packets.append(dict(zip(parsed_response['fields'], data_packet)))

        self.log_info(f"{PurpleairDataExtractor.__name__}: done")
        return data_packets

    def _exit_on_bad_parsed_response(self, parsed_response: Dict[str, Any]):
        if 'data' not in parsed_response:
            raise SystemExit(f"{PurpleairDataExtractor.__name__}: bad api response: missing 'data' item")
        if 'fields' not in parsed_response:
            raise SystemExit(f"{PurpleairDataExtractor.__name__}: bad api response: missing 'fields' item")


################################ THINGSPEAK DATA EXTRACTOR ################################
class ThingspeakDataExtractor(DataExtractor):

    def __init__(self, log_filename="app"):
        super(ThingspeakDataExtractor, self).__init__(log_filename=log_filename)

    @log_decorator.log_decorator()
    def extract(self, parsed_response: Dict[str, Any], channel_name="") -> List[Dict[str, Any]]:

        self.log_info(f"{ThingspeakDataExtractor.__name__}: try to extract API sensor data...")

        if channel_name == adapt_const.FST_CH_A:
            field_to_use = api_const.THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_1A
        elif channel_name == adapt_const.FST_CH_B:
            field_to_use = api_const.THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_1B
        elif channel_name == adapt_const.SND_CH_A:
            field_to_use = api_const.THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_2A
        elif channel_name == adapt_const.SND_CH_B:
            field_to_use = api_const.THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_2B
        else:
            raise SystemExit(f"{ThingspeakDataExtractor.__name__}: bad parameter => invalid channel_name='{channel_name}'")

        # Check parsed response correct shape
        if 'feeds' not in parsed_response:
            raise SystemExit(f"{ThingspeakDataExtractor.__name__}: bad api response: missing 'feeds' item")

        data_packets = []
        for feed in parsed_response['feeds']:
            self._exit_on_bad_parsed_response(feed)
            data_packet = {'created_at': feed['created_at'], api_const.FIELDS: []}
            for field in field_to_use.keys():
                data_packet[api_const.FIELDS].append({api_const.FIELD_NAME: field_to_use[field], api_const.FIELD_VALUE: feed[field]})
            data_packets.append(data_packet)

        self.log_info(f"{ThingspeakDataExtractor.__name__}: done")
        return data_packets

    def _exit_on_bad_parsed_response(self, parsed_response: Dict[str, Any]):
        if 'created_at' not in parsed_response:
            raise SystemExit(f"{ThingspeakDataExtractor.__name__}: bad api response: missing 'created_at' item")


################################ ATMOTUBE DATA EXTRACTOR ################################

class AtmotubeDataExtractor(DataExtractor):

    def __init__(self, log_filename="app"):
        super(AtmotubeDataExtractor, self).__init__(log_filename=log_filename)

    @log_decorator.log_decorator()
    def extract(self, parsed_response: Dict[str, Any], channel_name="") -> List[Dict[str, Any]]:

        self.log_info(f"{AtmotubeDataExtractor.__name__}: try to extract API sensor data...")
        self._exit_on_bad_parsed_response(parsed_response=parsed_response)
        sensor_data = parsed_response['data']['items']
        self.log_info(f"{AtmotubeDataExtractor.__name__}: done")
        return sensor_data

    def _exit_on_bad_parsed_response(self, parsed_response: Dict[str, Any]):
        if 'data' not in parsed_response:
            raise SystemExit(f"{AtmotubeDataExtractor.__name__}: bad api response: missing 'data' item")
        if 'items' not in parsed_response['data']:
            raise SystemExit(f"{AtmotubeDataExtractor.__name__}: bad api response: 'data' item miss 'items' list.")
