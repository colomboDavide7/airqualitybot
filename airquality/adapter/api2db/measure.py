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
PAR_NAME = 'param_name'
PAR_VAL = 'param_value'


def get_measure_adapter(sensor_type: str, timestamp_class):
    if sensor_type == 'atmotube':
        return AtmotubeMeasureAdapter(timestamp_class)
    elif sensor_type == 'thingspeak':
        return ThingspeakMeasureAdapter(timestamp_class)
    else:
        return None


class MeasureAdapter(abc.ABC):

    def __init__(self, timestamp_cls):
        self.timestamp_cls = timestamp_cls

    @abc.abstractmethod
    def reshape(self, data: Dict[str, Any]) -> Dict[str, Any]:
        pass


class AtmotubeMeasureAdapter(MeasureAdapter):

    def __init__(self, timestamp_cls):
        super(AtmotubeMeasureAdapter, self).__init__(timestamp_cls=timestamp_cls)

    def reshape(self, data: Dict[str, Any]) -> Dict[str, Any]:
        uniformed_data = {}
        try:
            if data.get('coords') is not None:
                uniformed_data[LAT] = data['coords']['lat']
                uniformed_data[LNG] = data['coords']['lon']
            uniformed_data[TS] = self.timestamp_cls(data['time'])
            uniformed_data[PAR_NAME] = ['voc', 'pm1', 'pm25', 'pm10', 't', 'h', 'p']
            uniformed_data[PAR_VAL] = [data.get('voc'), data.get('pm1'), data.get('pm25'),
                                       data.get('pm10'), data.get('t'), data.get('h'),
                                       data.get('p')]
        except KeyError as ke:
            raise SystemExit(f"{AtmotubeMeasureAdapter.__name__}: bad data packet => missing key={ke!s}")
        return uniformed_data


class ThingspeakMeasureAdapter(MeasureAdapter):

    def __init__(self, timestamp_cls):
        super(ThingspeakMeasureAdapter, self).__init__(timestamp_cls=timestamp_cls)

    def reshape(self, data: Dict[str, Any]) -> Dict[str, Any]:
        uniformed_data = {}
        try:
            uniformed_data[TS] = self.timestamp_cls(data['created_at'])
            param_name = []
            param_value = []
            for field in data['fields']:
                param_name.append(field['name'])
                param_value.append(field['value'])
            uniformed_data[PAR_NAME] = param_name
            uniformed_data[PAR_VAL] = param_value

        except KeyError as ke:
            raise SystemExit(f"{ThingspeakMeasureAdapter.__name__}: bad data packet => missing key={ke!s}")
        return uniformed_data
