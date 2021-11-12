######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
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


def get_measure_reshaper_class(sensor_type: str):

    if sensor_type == 'atmotube':
        return AtmotubeMeasureReshaper
    elif sensor_type == 'thingspeak':
        return ThingspeakMeasureReshaper
    else:
        raise SystemExit(f"'{get_measure_reshaper_class.__name__}()': "
                         f"bad type => {MeasureReshaper.__name__} undefined for type='{sensor_type}'")


class MeasureReshaper(abc.ABC):

    def __init__(self, data_packet: Dict[str, Any]):
        self.packet = data_packet

    @abc.abstractmethod
    def reshape(self) -> Dict[str, Any]:
        pass


class AtmotubeMeasureReshaper(MeasureReshaper):

    def __init__(self, data_packet: Dict[str, Any]):
        super(AtmotubeMeasureReshaper, self).__init__(data_packet)

    def reshape(self) -> Dict[str, Any]:
        uniformed_packet = {}
        try:
            if self.packet.get('coords') is not None:
                uniformed_packet[LAT] = self.packet['coords']['lat']
                uniformed_packet[LNG] = self.packet['coords']['lon']
            uniformed_packet[TS] = self.packet['time']
            uniformed_packet[PAR_NAME] = ['voc', 'pm1', 'pm25', 'pm10', 't', 'h', 'p']
            uniformed_packet[PAR_VAL] = [self.packet.get('voc'), self.packet.get('pm1'), self.packet.get('pm25'),
                                         self.packet.get('pm10'), self.packet.get('t'), self.packet.get('h'),
                                         self.packet.get('p')]
        except KeyError as ke:
            raise SystemExit(f"{AtmotubeMeasureReshaper.__name__}: bad data packet => missing key={ke!s}")
        return uniformed_packet


class ThingspeakMeasureReshaper(MeasureReshaper):

    def __init__(self, data_packet: Dict[str, Any]):
        super(ThingspeakMeasureReshaper, self).__init__(data_packet)

    def reshape(self) -> Dict[str, Any]:
        uniformed_packet = {}
        try:
            uniformed_packet[TS] = self.packet['created_at']
            param_name = []
            param_value = []
            for field in self.packet['fields']:
                param_name.append(field['name'])
                param_value.append(field['value'])
            uniformed_packet[PAR_NAME] = param_name
            uniformed_packet[PAR_VAL] = param_value

        except KeyError as ke:
            raise SystemExit(f"{ThingspeakMeasureReshaper.__name__}: bad data packet => missing key={ke!s}")
        return uniformed_packet
