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


def get_api2db_reshaper_class(sensor_type: str):

    if sensor_type == 'purpleair':
        return PurpleairUniformReshaper
    elif sensor_type == 'atmotube':
        return AtmotubeUniformReshaper
    elif sensor_type == 'thingspeak':
        return ThingspeakUniformReshaper


class UniformReshaper(abc.ABC):

    def __init__(self, packet: Dict[str, Any]):
        self.packet = packet

    @abc.abstractmethod
    def reshape(self) -> Dict[str, Any]:
        pass


class PurpleairUniformReshaper(UniformReshaper):

    def __init__(self, packet: Dict[str, Any]):
        super(PurpleairUniformReshaper, self).__init__(packet)

    def reshape(self) -> Dict[str, Any]:
        universal_packet = {}
        try:
            corrected_name = self.packet['name'].replace("'", "")
            universal_packet[NAME] = f"{corrected_name} ({self.packet['sensor_index']})"
            universal_packet[TYPE] = 'PurpleAir/ThingSpeak'
            universal_packet[LAT] = self.packet['latitude']
            universal_packet[LNG] = self.packet['longitude']
            universal_packet[PAR_NAME] = ['primary_id_a',
                                          'primary_id_b',
                                          'primary_key_a',
                                          'primary_key_b',
                                          'secondary_id_a',
                                          'secondary_id_b',
                                          'secondary_key_a',
                                          'secondary_key_b']
            universal_packet[PAR_VAL] = [self.packet['primary_id_a'],
                                         self.packet['primary_id_b'],
                                         self.packet['primary_key_a'],
                                         self.packet['primary_key_b'],
                                         self.packet['secondary_id_a'],
                                         self.packet['secondary_id_b'],
                                         self.packet['secondary_key_a'],
                                         self.packet['secondary_key_b']]
        except KeyError as ke:
            # Raise Exception if any key is missing from the 'packet' dictionary
            raise SystemExit(f"{PurpleairUniformReshaper.__name__} is missing the key={ke!s}.")
        return universal_packet


class AtmotubeUniformReshaper(UniformReshaper):

    def __init__(self, packet: Dict[str, Any]):
        super(AtmotubeUniformReshaper, self).__init__(packet)

    def reshape(self) -> Dict[str, Any]:
        universal_packet = {}
        try:
            if self.packet.get('coords') is not None:
                universal_packet[LAT] = self.packet['coords']['lat']
                universal_packet[LNG] = self.packet['coords']['lon']
            universal_packet[TS] = self.packet['time']
            universal_packet[PAR_NAME] = ['voc',
                                          'pm1',
                                          'pm25',
                                          'pm10',
                                          't',
                                          'h',
                                          'p']
            universal_packet[PAR_VAL] = [self.packet.get('voc'),
                                         self.packet.get('pm1'),
                                         self.packet.get('pm25'),
                                         self.packet.get('pm10'),
                                         self.packet.get('t'),
                                         self.packet.get('h'),
                                         self.packet.get('p')]
        except KeyError as ke:
            # Raise Exception if any key is missing from the 'packet' dictionary
            raise SystemExit(f"{PurpleairUniformReshaper.__name__} is missing the key={ke!s}.")
        return universal_packet


class ThingspeakUniformReshaper(UniformReshaper):

    def __init__(self, packet: Dict[str, Any]):
        super(ThingspeakUniformReshaper, self).__init__(packet)

    def reshape(self) -> Dict[str, Any]:
        universal_packet = {}
        try:
            universal_packet[TS] = self.packet['created_at']
            param_name = []
            param_value = []
            for field in self.packet['fields']:
                param_name.append(field['name'])
                param_value.append(field['value'])
            universal_packet[PAR_NAME] = param_name
            universal_packet[PAR_VAL] = param_value

        except KeyError as ke:
            # Raise Exception if any key is missing from the 'packet' dictionary
            raise SystemExit(f"{ThingspeakUniformReshaper.__name__} is missing the key={ke!s}.")
        return universal_packet
