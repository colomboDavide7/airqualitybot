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


def get_sensor_adapter(sensor_type: str):
    if sensor_type == 'purpleair':
        return PurpleairSensorAdapter()
    else:
        raise SystemExit(f"'{get_sensor_adapter.__name__}():' bad type '{sensor_type}'")


class SensorAdapter(abc.ABC):

    @abc.abstractmethod
    def reshape(self, sensor_data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abc.abstractmethod
    def _add_sensor_name(self, uniformed_data: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abc.abstractmethod
    def _add_sensor_info(self, uniformed_data: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abc.abstractmethod
    def _add_api_param(self, uniformed_data: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        pass


class PurpleairSensorAdapter(SensorAdapter):
    SENSOR_TYPE = 'PurpleAir/ThingSpeak'
    CHANNEL_NAMES = ["1A", "1B", "2A", "2B"]
    API_PARAM = ['primary_id_a', 'primary_id_b', 'primary_key_a', 'primary_key_b',
                 'secondary_id_a', 'secondary_id_b', 'secondary_key_a', 'secondary_key_b']

    def reshape(self, data: Dict[str, Any]) -> Dict[str, Any]:
        uniformed_data = {}
        try:
            uniformed_data = self._add_sensor_name(uniformed_data=uniformed_data, data=data)
            uniformed_data = self._add_sensor_info(uniformed_data=uniformed_data, data=data)
            uniformed_data = self._add_location(uniformed_data=uniformed_data, data=data)
            uniformed_data = self._add_api_param(uniformed_data=uniformed_data, data=data)
            uniformed_data[TYPE] = PurpleairSensorAdapter.SENSOR_TYPE
        except KeyError as ke:
            raise SystemExit(f"{PurpleairSensorAdapter.__name__}: bad sensor data => missing key={ke!s}")
        return uniformed_data

    def _add_sensor_name(self, uniformed_data: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        db_safe_name = data['name'].replace("'", "")
        uniformed_data[NAME] = f"{db_safe_name} ({data['sensor_index']})"
        return uniformed_data

    def _add_sensor_info(self, uniformed_data: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        last_ts = []
        ch_names = []
        for name in PurpleairSensorAdapter.CHANNEL_NAMES:
            ch_names.append(name)
            last_ts.append({TS: data['date_created']})
        uniformed_data[LAST] = last_ts
        uniformed_data[CHANNEL] = ch_names
        return uniformed_data

    def _add_api_param(self, uniformed_data: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        param_name = []
        param_value = []
        for name in PurpleairSensorAdapter.API_PARAM:
            param_name.append(name)
            param_value.append(data[name])
        uniformed_data[PAR_VAL] = param_value
        uniformed_data[PAR_NAME] = param_name
        return uniformed_data

    def _add_location(self, uniformed_data: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        uniformed_data[LAT] = data['latitude']
        uniformed_data[LNG] = data['longitude']
        return uniformed_data
