######################################################
#
# Author: Davide Colombo
# Date: 12/11/21 17:20
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import Dict, Any
import airquality.database.operation.select.type as sel

TS = 'timestamp'
LAT = 'lat'
LNG = 'lng'
PARAM = 'param'
PAR_ID = 'id'
PAR_VAL = 'val'
REC_ID = 'record_id'


def get_measure_adapter(sensor_type: str, type_wrapper: sel.TypeSelectWrapper):

    if sensor_type == 'atmotube':
        return AtmotubeMeasureAdapter(type_wrapper=type_wrapper)
    elif sensor_type == 'thingspeak':
        return ThingspeakMeasureAdapter(type_wrapper=type_wrapper)
    else:
        raise SystemExit(f"'{get_measure_adapter.__name__}():' bad type '{sensor_type}'")


################################ INJECT ADAPTER DEPENDENCIES ################################
class MeasureAdapter(abc.ABC):

    def __init__(self, type_wrapper: sel.TypeSelectWrapper):
        self.measure_param_map = type_wrapper.get_measure_param()

    @abc.abstractmethod
    def reshape(self, data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abc.abstractmethod
    def _add_param_id_param_value(self, uniformed_data: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abc.abstractmethod
    def _add_record_id(self, uniformed_data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abc.abstractmethod
    def _exit_on_bad_sensor_data(self, data: Dict[str, Any]):
        pass


################################ INJECT ADAPTER DEPENDENCIES ################################
class AtmotubeMeasureAdapter(MeasureAdapter):

    ATMOTUBE_PARAM_NAMES = ['voc', 'pm1', 'pm25', 'pm10', 't', 'h', 'p']

    def __init__(self, type_wrapper: sel.TypeSelectWrapper):
        super(AtmotubeMeasureAdapter, self).__init__(type_wrapper=type_wrapper)
        self.record_id = type_wrapper.get_max_record_id()

    def _exit_on_bad_sensor_data(self, data: Dict[str, Any]):
        if 'time' not in data:
            raise SystemExit(f"{AtmotubeMeasureAdapter.__name__}: bad sensor data => missing key='time'")

    def reshape(self, data: Dict[str, Any]) -> Dict[str, Any]:
        self._exit_on_bad_sensor_data(data=data)
        uniformed_data = {}
        uniformed_data = self._add_record_id(uniformed_data=uniformed_data)
        uniformed_data = self._add_param_id_param_value(uniformed_data=uniformed_data, data=data)
        uniformed_data = self._add_geometry(uniformed_data=uniformed_data, data=data)
        uniformed_data[TS] = data['time']
        self.record_id += 1
        return uniformed_data

    def _add_record_id(self, uniformed_data: Dict[str, Any]) -> Dict[str, Any]:
        uniformed_data[REC_ID] = self.record_id
        return uniformed_data

    def _add_param_id_param_value(self, uniformed_data: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        uniformed_data[PARAM] = [{PAR_ID: self.measure_param_map[n], PAR_VAL: data.get(n)}
                                 for n in AtmotubeMeasureAdapter.ATMOTUBE_PARAM_NAMES]
        return uniformed_data

    def _add_geometry(self, uniformed_data: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        if data.get('coords') is not None:
            uniformed_data[LAT] = data['coords']['lat']
            uniformed_data[LNG] = data['coords']['lon']
        return uniformed_data


################################ INJECT ADAPTER DEPENDENCIES ################################
class ThingspeakMeasureAdapter(MeasureAdapter):

    def __init__(self, type_wrapper: sel.TypeSelectWrapper):
        super(ThingspeakMeasureAdapter, self).__init__(type_wrapper=type_wrapper)
        self.record_id = type_wrapper.get_max_record_id()

    def _exit_on_bad_sensor_data(self, data: Dict[str, Any]):
        if 'created_at' not in data:
            raise SystemExit(f"{ThingspeakMeasureAdapter.__name__}: bad sensor data => missing key='created_at'")
        if 'fields' not in data:
            raise SystemExit(f"{ThingspeakMeasureAdapter.__name__}: bad sensor data => missing key='fields'")
        for f in data['fields']:
            if 'name' not in f or 'value' not in f:
                raise SystemExit(f"{ThingspeakMeasureAdapter.__name__}: bad sensor data => fields must be a list of "
                                 f"dictionaries with 'name' and 'value' keys")

    def reshape(self, data: Dict[str, Any]) -> Dict[str, Any]:
        self._exit_on_bad_sensor_data(data=data)
        uniformed_data = {}
        uniformed_data = self._add_record_id(uniformed_data=uniformed_data)
        uniformed_data = self._add_param_id_param_value(uniformed_data=uniformed_data, data=data)
        uniformed_data[TS] = data['created_at']
        self.record_id += 1
        return uniformed_data

    def _add_record_id(self, uniformed_data: Dict[str, Any]) -> Dict[str, Any]:
        uniformed_data[REC_ID] = self.record_id
        return uniformed_data

    def _add_param_id_param_value(self, uniformed_data: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        uniformed_data[PARAM] = [{PAR_ID: self.measure_param_map[f['name']], PAR_VAL: f['value']} for f in data['fields']]
        return uniformed_data
