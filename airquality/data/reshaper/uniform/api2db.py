######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 06/11/21 09:19
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import Dict, Any

TS = 'timestamp'
NAME = 'name'
TYPE = 'type'
LAT = 'lat'
LNG = 'lng'
PAR_NAME = 'param_name'
PAR_VAL = 'param_value'


class UniformReshaper(abc.ABC):

    @abc.abstractmethod
    def api2db(self, packet: Dict[str, Any]) -> Dict[str, Any]:
        pass


class PurpleairUniformReshaper(UniformReshaper):

    def api2db(self, packet: Dict[str, Any]) -> Dict[str, Any]:
        universal_packet = {}
        try:
            corrected_name = packet['name'].replace("'", "")
            universal_packet[NAME] = f"{corrected_name} ({packet['sensor_index']})"
            universal_packet[TYPE] = 'PurpleAir/ThingSpeak'
            universal_packet[LAT] = packet['latitude']
            universal_packet[LNG] = packet['longitude']
            universal_packet[PAR_NAME] = ['primary_id_a',
                                          'primary_id_b',
                                          'primary_key_a',
                                          'primary_key_b',
                                          'secondary_id_a',
                                          'secondary_id_b',
                                          'secondary_key_a',
                                          'secondary_key_b']
            universal_packet[PAR_VAL] = [packet['primary_id_a'],
                                         packet['primary_id_b'],
                                         packet['primary_key_a'],
                                         packet['primary_key_b'],
                                         packet['secondary_id_a'],
                                         packet['secondary_id_b'],
                                         packet['secondary_key_a'],
                                         packet['secondary_key_b']]
        except KeyError as ke:
            # Raise Exception if any key is missing from the 'packet' dictionary
            raise SystemExit(f"{PurpleairUniformReshaper.__name__} is missing the key={ke!s}.")
        return universal_packet


class AtmotubeUniformReshaper(UniformReshaper):

    def api2db(self, packet: Dict[str, Any]) -> Dict[str, Any]:
        universal_packet = {}
        try:
            if packet.get('coords') is not None:
                universal_packet[LAT] = packet['coords']['lat']
                universal_packet[LNG] = packet['coords']['lon']
            universal_packet[TS] = packet['time']
            universal_packet[PAR_NAME] = ['voc',
                                          'pm1',
                                          'pm25',
                                          'pm10',
                                          't',
                                          'h',
                                          'p']
            universal_packet[PAR_VAL] = [packet.get('voc'),
                                         packet.get('pm1'),
                                         packet.get('pm25'),
                                         packet.get('pm10'),
                                         packet.get('t'),
                                         packet.get('h'),
                                         packet.get('p')]
        except KeyError as ke:
            # Raise Exception if any key is missing from the 'packet' dictionary
            raise SystemExit(f"{PurpleairUniformReshaper.__name__} is missing the key={ke!s}.")
        return universal_packet


class ThingspeakUniformReshaper(UniformReshaper):

    def api2db(self, packet: Dict[str, Any]) -> Dict[str, Any]:
        universal_packet = {}
        try:
            universal_packet[TS] = packet['created_at']
            param_name = []
            param_value = []
            for field in packet['fields']:
                param_name.append(field['name'])
                param_value.append(field['value'])
            universal_packet[PAR_NAME] = param_name
            universal_packet[PAR_VAL] = param_value

        except KeyError as ke:
            # Raise Exception if any key is missing from the 'packet' dictionary
            raise SystemExit(f"{ThingspeakUniformReshaper.__name__} is missing the key={ke!s}.")
        return universal_packet
