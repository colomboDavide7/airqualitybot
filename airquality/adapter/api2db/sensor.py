######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 12/11/21 17:28
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


def get_sensor_adapter_class(sensor_type: str):

    if sensor_type == 'purpleair':
        return PurpleairSensorAdapter
    else:
        raise SystemExit(f"'{get_sensor_adapter_class.__name__}()': "
                         f"bad type => {SensorAdapter.__name__} undefined for type='{sensor_type}'")


class SensorAdapter(abc.ABC):

    def __init__(self, sensor_data: Dict[str, Any]):
        self.packet = sensor_data

    @abc.abstractmethod
    def reshape(self) -> Dict[str, Any]:
        pass


class PurpleairSensorAdapter(SensorAdapter):

    def __init__(self, sensor_data: Dict[str, Any]):
        super(PurpleairSensorAdapter, self).__init__(sensor_data)

    def reshape(self) -> Dict[str, Any]:
        universal_packet = {}
        try:
            db_safe_name = self.packet['name'].replace("'", "")
            universal_packet[NAME] = f"{db_safe_name} ({self.packet['sensor_index']})"
            universal_packet[TYPE] = 'PurpleAir/ThingSpeak'
            universal_packet[LAT] = self.packet['latitude']
            universal_packet[LNG] = self.packet['longitude']
            universal_packet[PAR_NAME] = ['primary_id_a', 'primary_id_b', 'primary_key_a', 'primary_key_b',
                                          'secondary_id_a', 'secondary_id_b', 'secondary_key_a', 'secondary_key_b']
            universal_packet[PAR_VAL] = [self.packet['primary_id_a'], self.packet['primary_id_b'],
                                         self.packet['primary_key_a'], self.packet['primary_key_b'],
                                         self.packet['secondary_id_a'], self.packet['secondary_id_b'],
                                         self.packet['secondary_key_a'], self.packet['secondary_key_b']]
        except KeyError as ke:
            raise SystemExit(f"{PurpleairSensorAdapter.__name__}: bad sensor data => missing key={ke!s}")
        return universal_packet
