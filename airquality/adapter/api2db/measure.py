######################################################
#
# Author: Davide Colombo
# Date: 12/11/21 17:20
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
PAR_ID = 'param_id'
PAR_VAL = 'param_value'
REC_ID = 'record_id'


def get_measure_adapter(sensor_type: str, start_id: int, measure_param_map: Dict[str, Any]):
    if sensor_type == 'atmotube':
        return AtmotubeMeasureAdapter(start_id=start_id, measure_param_map=measure_param_map)
    elif sensor_type == 'thingspeak':
        return ThingspeakMeasureAdapter(start_id=start_id, measure_param_map=measure_param_map)
    else:
        raise SystemExit(f"'{get_measure_adapter.__name__}():' bad type '{sensor_type}'")


################################ INJECT ADAPTER DEPENDENCIES ################################
class MeasureAdapter(abc.ABC):

    def __init__(self, start_id: int, measure_param_map: Dict[str, Any]):
        self.measure_param_map = measure_param_map
        self.start_id = start_id

    @abc.abstractmethod
    def reshape(self, data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abc.abstractmethod
    def _add_param_id_param_value(self, uniformed_data: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    def _add_record_id_and_increment(self, uniformed_data: Dict[str, Any]) -> Dict[str, Any]:
        uniformed_data[REC_ID] = self.start_id
        self.start_id += 1
        return uniformed_data


################################ INJECT ADAPTER DEPENDENCIES ################################
class AtmotubeMeasureAdapter(MeasureAdapter):

    ATMOTUBE_PARAM_NAMES = ['voc', 'pm1', 'pm25', 'pm10', 't', 'h', 'p']

    def __init__(self, start_id: int, measure_param_map: Dict[str, Any]):
        super(AtmotubeMeasureAdapter, self).__init__(start_id=start_id, measure_param_map=measure_param_map)

    def reshape(self, data: Dict[str, Any]) -> Dict[str, Any]:

        uniformed_data = {}
        try:
            uniformed_data = self._add_record_id_and_increment(uniformed_data=uniformed_data)
            uniformed_data = self._add_param_id_param_value(uniformed_data=uniformed_data, data=data)
            uniformed_data = self._add_geometry(uniformed_data=uniformed_data, data=data)
            uniformed_data[TS] = data['time']
        except KeyError as ke:
            raise SystemExit(f"{AtmotubeMeasureAdapter.__name__}: bad sensor data => missing key={ke!s}")
        return uniformed_data

    def _add_param_id_param_value(self, uniformed_data: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        param_ids = []
        param_values = []
        for name in AtmotubeMeasureAdapter.ATMOTUBE_PARAM_NAMES:
            param_ids.append(self.measure_param_map[name])
            param_values.append(data.get(name))
        uniformed_data[PAR_ID] = param_ids
        uniformed_data[PAR_VAL] = param_values
        return uniformed_data

    def _add_geometry(self, uniformed_data: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        if data.get('coords') is not None:
            uniformed_data[LAT] = data['coords']['lat']
            uniformed_data[LNG] = data['coords']['lon']
        return uniformed_data


################################ INJECT ADAPTER DEPENDENCIES ################################
class ThingspeakMeasureAdapter(MeasureAdapter):

    def __init__(self, start_id: int, measure_param_map: Dict[str, Any]):
        super(ThingspeakMeasureAdapter, self).__init__(start_id=start_id, measure_param_map=measure_param_map)

    def reshape(self, data: Dict[str, Any]) -> Dict[str, Any]:
        uniformed_data = {}
        try:
            uniformed_data = self._add_record_id_and_increment(uniformed_data=uniformed_data)
            uniformed_data = self._add_param_id_param_value(uniformed_data=uniformed_data, data=data)
            uniformed_data[TS] = data['created_at']
        except KeyError as ke:
            raise SystemExit(f"{ThingspeakMeasureAdapter.__name__}: bad sensor data => missing key={ke!s}")
        return uniformed_data

    def _add_param_id_param_value(self, uniformed_data: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        param_ids = []
        param_value = []
        for field in data['fields']:
            param_id = self.measure_param_map[field['name']]
            param_ids.append(param_id)
            param_value.append(field['value'])
        uniformed_data[PAR_ID] = param_ids
        uniformed_data[PAR_VAL] = param_value
        return uniformed_data
