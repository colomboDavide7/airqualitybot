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
PARAM = 'param'
PAR_NAME = 'param_name'
PAR_VAL = 'param_value'
INFO = 'info'
CHANNEL = 'channel'
LAST = 'last_acquisition'


def get_sensor_adapter(sensor_type: str):
    if sensor_type == 'purpleair':
        return PurpleairSensorAdapter()
    else:
        raise SystemExit(f"'{get_sensor_adapter.__name__}():' bad type '{sensor_type}'")


################################ SENSOR ADAPTER CLASS ################################
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

    @abc.abstractmethod
    def _exit_on_bad_sensor_data(self, sensor_data: Dict[str, Any]):
        pass


################################ PURPLEAIR SENSOR ADAPTER ################################
class PurpleairSensorAdapter(SensorAdapter):

    SENSOR_TYPE = 'PurpleAir/ThingSpeak'
    CHANNEL_NAMES = ["1A", "1B", "2A", "2B"]
    API_PARAM = ['primary_id_a', 'primary_id_b', 'primary_key_a', 'primary_key_b',
                 'secondary_id_a', 'secondary_id_b', 'secondary_key_a', 'secondary_key_b']

    def reshape(self, data: Dict[str, Any]) -> Dict[str, Any]:
        self._exit_on_bad_sensor_data(sensor_data=data)
        uniformed_data = {}
        uniformed_data = self._add_sensor_name(uniformed_data=uniformed_data, data=data)
        uniformed_data = self._add_sensor_info(uniformed_data=uniformed_data, data=data)
        uniformed_data = self._add_location(uniformed_data=uniformed_data, data=data)
        uniformed_data = self._add_api_param(uniformed_data=uniformed_data, data=data)
        uniformed_data[TYPE] = PurpleairSensorAdapter.SENSOR_TYPE
        return uniformed_data

    def _exit_on_bad_sensor_data(self, sensor_data: Dict[str, Any]):
        if 'name' not in sensor_data or 'sensor_index' not in sensor_data:
            raise SystemExit(f"{PurpleairSensorAdapter.__name__}: bad sensor data => missing sensor key")
        if 'latitude' not in sensor_data or 'longitude' not in sensor_data:
            raise SystemExit(f"{PurpleairSensorAdapter.__name__}: bad sensor data => missing geolocation key")
        if 'date_created' not in sensor_data:
            raise SystemExit(f"{PurpleairSensorAdapter.__name__}: bad sensor data => missing sensor info key")
        for n in PurpleairSensorAdapter.API_PARAM:
            if n not in sensor_data:
                raise SystemExit(f"{PurpleairSensorAdapter.__name__}: bad sensor data => missing api param key='{n}'")

    def _add_sensor_name(self, uniformed_data: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        db_safe_name = data['name'].replace("'", "")
        uniformed_data[NAME] = f"{db_safe_name} ({data['sensor_index']})"
        return uniformed_data

    def _add_sensor_info(self, uniformed_data: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        uniformed_data[INFO] = [{CHANNEL: n, TS: data['date_created']} for n in PurpleairSensorAdapter.CHANNEL_NAMES]
        return uniformed_data

    def _add_api_param(self, uniformed_data: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        uniformed_data[PARAM] = [{PAR_NAME: n, PAR_VAL: data[n]} for n in PurpleairSensorAdapter.API_PARAM]
        return uniformed_data

    def _add_location(self, uniformed_data: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        uniformed_data[LAT] = data['latitude']
        uniformed_data[LNG] = data['longitude']
        return uniformed_data
