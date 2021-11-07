######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 07/11/21 15:30
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any
from abc import ABC, abstractmethod
from airquality.constants.shared_constants import EXCEPTION_HEADER


class MeasurementAdapter(ABC):

    def __init__(self, measure_param_map: Dict[str, Any]):
        self.measure_param_map = measure_param_map

    @abstractmethod
    def adapt(self, packet: Dict[str, Any]) -> Dict[str, Any]:
        pass


class MeasurementAdapterAtmotube(MeasurementAdapter):

    def __init__(self, measure_param_map: Dict[str, Any]):
        super().__init__(measure_param_map)

    def adapt(self, packet: Dict[str, Any]) -> Dict[str, Any]:
        adapted_packet = {}
        try:
            adapted_packet['timestamp'] = packet['timestamp']
            adapted_packet['geom'] = packet['geom']
            adapted_packet['param_id'] = [self.measure_param_map['voc'],
                                          self.measure_param_map['pm1'],
                                          self.measure_param_map['pm25'],
                                          self.measure_param_map['pm10'],
                                          self.measure_param_map['t'],
                                          self.measure_param_map['h'],
                                          self.measure_param_map['p']]
            adapted_packet['param_val'] = [packet.get('voc'),
                                           packet.get('pm1'),
                                           packet.get('pm25'),
                                           packet.get('pm10'),
                                           packet.get('t'),
                                           packet.get('h'),
                                           packet.get('p')]
        except KeyError as ke:
            raise SystemExit(f"{EXCEPTION_HEADER} {MeasurementAdapterAtmotube.__name__} is missing the key={ke!s}.")
        return adapted_packet


class MeasurementAdapterThingspeak(MeasurementAdapter):

    def __init__(self, measure_param_map: Dict[str, Any]):
        super().__init__(measure_param_map)

    def adapt(self, packet: Dict[str, Any]) -> Dict[str, Any]:
        adapted_packet = {}
        try:
            adapted_packet['timestamp'] = packet['timestamp']
            param_id = []
            param_val = []
            for field in packet['fields']:
                param_val.append(field['val'])
                name = field['name']
                param_id.append(self.measure_param_map[name])
            adapted_packet['param_id'] = param_id
            adapted_packet['param_val'] = param_val
        except KeyError as ke:
            raise SystemExit(f"{EXCEPTION_HEADER} {MeasurementAdapterThingspeak.__name__} is missing the key={ke!s}.")
        return adapted_packet


class MeasurementAdapterFactory(object):

    def __init__(self, adapter_class=MeasurementAdapter):
        self.adapter_class = adapter_class

    def make_adapter(self, measure_param_map: Dict[str, Any]):
        return self.adapter_class(measure_param_map)
