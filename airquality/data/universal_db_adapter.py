######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 06/11/21 09:19
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any
from abc import ABC, abstractmethod
from airquality.constants.shared_constants import EXCEPTION_HEADER
from utility.datetime_parser import DatetimeParser


class UniversalDatabaseAdapter(ABC):

    @abstractmethod
    def adapt(self, packet: Dict[str, Any]) -> Dict[str, Any]:
        pass


class PurpleairUniversalDatabaseAdapter(UniversalDatabaseAdapter):

    def adapt(self, packet: Dict[str, Any]) -> Dict[str, Any]:
        universal_packet = {}
        try:
            corrected_name = packet['name'].replace("'", "")
            universal_packet['name'] = f"{corrected_name} ({packet['sensor_index']})"
            universal_packet['type'] = 'PurpleAir/ThingSpeak'
            universal_packet['lat'] = packet['latitude']
            universal_packet['lng'] = packet['longitude']
            universal_packet['param_name'] = ['primary_id_a',
                                              'primary_id_b',
                                              'primary_key_a',
                                              'primary_key_b',
                                              'secondary_id_a',
                                              'secondary_id_b',
                                              'secondary_key_a',
                                              'secondary_key_b']
            universal_packet['param_value'] = [packet['primary_id_a'],
                                               packet['primary_id_b'],
                                               packet['primary_key_a'],
                                               packet['primary_key_b'],
                                               packet['secondary_id_a'],
                                               packet['secondary_id_b'],
                                               packet['secondary_key_a'],
                                               packet['secondary_key_b']]
        except KeyError as ke:
            # Raise Exception if any key is missing from the 'packet' dictionary
            raise SystemExit(
                f"{EXCEPTION_HEADER} {PurpleairUniversalDatabaseAdapter.__name__} is missing the key={ke!s}.")
        return universal_packet


class AtmotubeUniversalDatabaseAdapter(UniversalDatabaseAdapter):

    def adapt(self, packet: Dict[str, Any]) -> Dict[str, Any]:
        universal_packet = {}
        try:
            if packet.get('coords') is not None:
                universal_packet['lat'] = packet['coords']['lat']
                universal_packet['lng'] = packet['coords']['lon']
            universal_packet['timestamp'] = DatetimeParser.atmotube_to_sqltimestamp(packet['time'])
            universal_packet['param_name'] = ['voc',
                                              'pm1',
                                              'pm25',
                                              'pm10',
                                              't',
                                              'h',
                                              'p']
            universal_packet['param_value'] = [packet.get('voc'),
                                               packet.get('pm1'),
                                               packet.get('pm25'),
                                               packet.get('pm10'),
                                               packet.get('t'),
                                               packet.get('h'),
                                               packet.get('p')]
        except KeyError as ke:
            # Raise Exception if any key is missing from the 'packet' dictionary
            raise SystemExit(
                f"{EXCEPTION_HEADER} {PurpleairUniversalDatabaseAdapter.__name__} is missing the key={ke!s}.")
        return universal_packet


class ThingspeakUniversalDatabaseAdapter(UniversalDatabaseAdapter):

    def adapt(self, packet: Dict[str, Any]) -> Dict[str, Any]:
        universal_packet = {}
        try:
            universal_packet['timestamp'] = DatetimeParser.thingspeak_to_sqltimestamp(packet['created_at'])
            param_name = []
            param_value = []
            for field in packet['fields']:
                param_name.append(field['name'])
                param_value.append(field['value'])
            universal_packet['param_name'] = param_name
            universal_packet['param_value'] = param_value

        except KeyError as ke:
            # Raise Exception if any key is missing from the 'packet' dictionary
            raise SystemExit(f"{EXCEPTION_HEADER} {ThingspeakUniversalDatabaseAdapter.__name__} is missing the key={ke!s}.")
        return universal_packet
