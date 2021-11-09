#################################################
#
# @Author: davidecolombo
# @Date: lun, 25-10-2021, 10:54
# @Description: this script defines the classes for dynamically reshaping packets from sensor's API
#
#################################################
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from airquality.constants.shared_constants import EXCEPTION_HEADER

THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_1A = {"PM1.0 (ATM)": "pm1.0_atm_a", "PM2.5 (ATM)": "pm2.5_atm_a",
                                             "PM10.0 (ATM)": "pm10.0_atm_a", "Temperature": "temperature_a",
                                             "Humidity": "humidity_a"}
THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_1B = {"PM1.0 (ATM)": "pm1.0_atm_b", "PM2.5 (ATM)": "pm2.5_atm_b",
                                             "PM10.0 (ATM)": "pm10.0_atm_b", "Pressure": "pressure_b"}
THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_2A = {"0.3um": "0.3_um_count_a", "0.5um": "0.5_um_count_a",
                                             "1.0um": "1.0_um_count_a", "2.5um": "2.5_um_count_a",
                                             "5.0um": "5.0_um_count_a", "10.0um": "10.0_um_count_a"}
THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_2B = {"0.3um": "0.3_um_count_b", "0.5um": "0.5_um_count_b",
                                             "1.0um": "1.0_um_count_b", "2.5um": "2.5_um_count_b",
                                             "5.0um": "5.0_um_count_b", "10.0um": "10.0_um_count_b"}


################################ ABSTRACT BASE CLASS ################################
class PacketReshaper(ABC):

    @abstractmethod
    def reshape_packet(self, api_answer: Dict[str, Any]) -> List[Dict[str, Any]]:
        pass


################################ PURPLEAIR PACKET RESHAPER ################################
class PurpleairPacketReshaper(PacketReshaper):

    def reshape_packet(self, api_answer: Dict[str, Any]) -> List[Dict[str, Any]]:

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

        feeds: List[Dict[str, Any]] = api_answer['feeds']
        if not feeds:
            return []

        channel: Dict[str, Any] = api_answer['channel']
        sensor_name: str = channel['name']

        if not sensor_name.startswith('AirMonitor'):
            raise SystemExit(
                f"{EXCEPTION_HEADER} {ThingspeakPacketReshaper.__name__} bad name => expected a name that starts with "
                f"'AirMonitor', got name='{sensor_name}'."
        )

        # SELECT THE RESHAPE MAPPING BASED ON PRIMARY/SECONDARY DATA AND CHANNEL A/B
        if '_b' in sensor_name:
            if 'Counters' in sensor_name:
                field_to_use = THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_2B
            else:
                field_to_use = THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_1B
        else:
            if 'Counters' in sensor_name:
                field_to_use = THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_2A
            else:
                field_to_use = THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_1A

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
