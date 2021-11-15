######################################################
#
# Author: Davide Colombo
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
GEOM = 'geom'
PAR_NAME = 'param_name'
PAR_VAL = 'param_value'
CHANNEL = 'channel'
LAST = 'last_acquisition'


def get_sensor_adapter(sensor_type: str, postgis_class):
    if sensor_type == 'purpleair':
        return PurpleairSensorAdapter(postgis_class)
    else:
        return None


class SensorAdapter(abc.ABC):

    def __init__(self, postgis_class):
        self.postgis_class = postgis_class

    @abc.abstractmethod
    def reshape(self, sensor_data: Dict[str, Any]) -> Dict[str, Any]:
        pass


class PurpleairSensorAdapter(SensorAdapter):

    def __init__(self, postgis_class):
        super(PurpleairSensorAdapter, self).__init__(postgis_class)

    def reshape(self, data: Dict[str, Any]) -> Dict[str, Any]:
        uniformed_data = {}
        try:
            db_safe_name = data['name'].replace("'", "")
            uniformed_data[NAME] = f"{db_safe_name} ({data['sensor_index']})"
            uniformed_data[TYPE] = 'PurpleAir/ThingSpeak'
            geom_data = {LAT: data['latitude'], LNG: data['longitude']}
            uniformed_data[GEOM] = self.postgis_class(geom_data)
            uniformed_data[PAR_NAME] = ['primary_id_a', 'primary_id_b', 'primary_key_a', 'primary_key_b',
                                        'secondary_id_a', 'secondary_id_b', 'secondary_key_a', 'secondary_key_b']
            uniformed_data[PAR_VAL] = [data['primary_id_a'], data['primary_id_b'],
                                       data['primary_key_a'], data['primary_key_b'],
                                       data['secondary_id_a'], data['secondary_id_b'],
                                       data['secondary_key_a'], data['secondary_key_b']]
            uniformed_data[CHANNEL] = ["1A", "1B", "2A", "2B"]
            uniformed_data[LAST] = [data['date_created'], data['date_created'],
                                    data['date_created'], data['date_created']]
        except KeyError as ke:
            raise SystemExit(f"{PurpleairSensorAdapter.__name__}: bad sensor data => missing key={ke!s}")
        return uniformed_data
