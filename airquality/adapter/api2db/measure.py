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
PAR_VAL = 'param_value'
REC_ID = 'record_id'


def get_measure_adapter(sensor_type: str, timestamp_class, start_id: int):
    if sensor_type == 'atmotube':
        return AtmotubeMeasureAdapter(timestamp_class, start_id=start_id)
    elif sensor_type == 'thingspeak':
        return ThingspeakMeasureAdapter(timestamp_class, start_id=start_id)
    else:
        raise SystemExit(f"'{get_measure_adapter.__name__}():' bad type '{sensor_type}'")


class MeasureAdapter(abc.ABC):

    def __init__(self, timestamp_cls, start_id: int):
        self.timestamp_cls = timestamp_cls
        self.start_id = start_id

    @abc.abstractmethod
    def reshape(self, data: Dict[str, Any]) -> Dict[str, Any]:
        pass


class AtmotubeMeasureAdapter(MeasureAdapter):

    def __init__(self, timestamp_cls, start_id: int):
        super(AtmotubeMeasureAdapter, self).__init__(timestamp_cls=timestamp_cls, start_id=start_id)
        self.postgis_class = None

    def set_postgis_class(self, postgis_class):
        self.postgis_class = postgis_class

    def reshape(self, data: Dict[str, Any]) -> Dict[str, Any]:

        if self.postgis_class is None:
            raise SystemExit(f"{AtmotubeMeasureAdapter.__name__}: bad setup => missing external dependency 'postgis_class'")

        uniformed_data = {}
        try:
            uniformed_data[REC_ID] = self.start_id
            self.start_id += 1
            uniformed_data[GEOM] = None
            if data.get('coords') is not None:
                geom_data = {LAT: data['coords']['lat'], LNG: data['coords']['lon']}
                uniformed_data[GEOM] = self.postgis_class(geom_data).geom_from_text()
            uniformed_data[TS] = self.timestamp_cls(data['time'])
            uniformed_data[PAR_NAME] = ['voc', 'pm1', 'pm25', 'pm10', 't', 'h', 'p']
            uniformed_data[PAR_VAL] = [data.get('voc'), data.get('pm1'), data.get('pm25'),
                                       data.get('pm10'), data.get('t'), data.get('h'),
                                       data.get('p')]
        except KeyError as ke:
            raise SystemExit(f"{AtmotubeMeasureAdapter.__name__}: bad data packet => missing key={ke!s}")
        return uniformed_data


class ThingspeakMeasureAdapter(MeasureAdapter):

    def __init__(self, timestamp_cls, start_id: int):
        super(ThingspeakMeasureAdapter, self).__init__(timestamp_cls=timestamp_cls, start_id=start_id)

    def reshape(self, data: Dict[str, Any]) -> Dict[str, Any]:
        uniformed_data = {}
        try:
            uniformed_data[TS] = self.timestamp_cls(data['created_at'])
            uniformed_data[REC_ID] = self.start_id
            self.start_id += 1
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
