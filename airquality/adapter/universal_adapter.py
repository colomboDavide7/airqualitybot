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


class UniversalAdapter(ABC):

    @abstractmethod
    def adapt(self, packet: Dict[str, Any]) -> Dict[str, Any]:
        pass


class PurpleairUniversalAdapter(UniversalAdapter):

    def adapt(self, packet: Dict[str, Any]) -> Dict[str, Any]:
        new_packet = {}
        try:
            corrected_name = packet['name'].replace("'", "")
            new_packet['name'] = f"{corrected_name} ({packet['sensor_index']})"
            new_packet['type'] = 'PurpleAir/ThingSpeak'
            new_packet['lat'] = packet['latitude']
            new_packet['lng'] = packet['longitude']
            new_packet['param_name'] = ['primary_id_a',
                                        'primary_id_b',
                                        'primary_key_a',
                                        'primary_key_b',
                                        'secondary_id_a',
                                        'secondary_id_b',
                                        'secondary_key_a',
                                        'secondary_key_b',
                                        'primary_timestamp_a',
                                        'primary_timestamp_b',
                                        'secondary_timestamp_a',
                                        'secondary_timestamp_b']
            new_packet['param_value'] = [packet['primary_id_a'],
                                         packet['primary_id_b'],
                                         packet['primary_key_a'],
                                         packet['primary_key_b'],
                                         packet['secondary_id_a'],
                                         packet['secondary_id_b'],
                                         packet['secondary_key_a'],
                                         packet['secondary_key_b'],
                                         '2018-01-01 00:00:00',
                                         '2018-01-01 00:00:00',
                                         '2018-01-01 00:00:00',
                                         '2018-01-01 00:00:00']
        except KeyError as ke:
            # Raise Exception if any key is missing from the 'packet' dictionary
            raise SystemExit(f"{EXCEPTION_HEADER} {PurpleairUniversalAdapter.__name__} is missing the key={ke!s}.")
        return new_packet
