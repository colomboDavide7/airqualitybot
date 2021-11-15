######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 05/11/21 17:37
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import Dict, Any


class RecordBuilder(abc.ABC):

    def __init__(self, sensor_id: int):
        self.sensor_id = sensor_id

    @abc.abstractmethod
    def record(self) -> str:
        pass


class LocationRecord(RecordBuilder):

    def __init__(self, sensor_id: int, valid_from: str, geom: str):
        super().__init__(sensor_id)
        self.valid_from = valid_from
        self.geom = geom

    def record(self) -> str:
        return f"({self.sensor_id}, '{self.valid_from}', {self.geom})"


class APIParamRecord(RecordBuilder):

    def __init__(self, sensor_id: int, packet: Dict[str, Any]):
        super().__init__(sensor_id)

        self.param_name = packet.get('param_name')
        self.param_value = packet.get('param_value')
        if not self.param_value or not self.param_name:
            raise SystemExit(f"{APIParamRecord.__name__}: bad packet => please check you packet has a non-empty list"
                             f"of param name(s) and a non-empty list of param value(s), one for each name(s).")
        if len(self.param_name) != len(self.param_value):
            raise SystemExit(f"{APIParamRecord.__name__}: bad packet => number of param name(s) does not match the "
                             f"number of param value(s)")

    def record(self) -> str:
        values = ','.join(f"({self.sensor_id}, '{n}', '{v}')" for n, v in zip(self.param_name, self.param_value))
        return values.strip(',')


class SensorRecord(RecordBuilder):

    def __init__(self, sensor_id: int, packet: Dict[str, Any]):
        super().__init__(sensor_id)
        try:
            self.sensor_name = packet['name']
            self.sensor_type = packet['type']
        except KeyError as ke:
            raise SystemExit(f"{SensorRecord.__name__} bad parameters => missing key={ke!s}.")

    def record(self) -> str:
        return f"('{self.sensor_type}', '{self.sensor_name}')"


class SensorInfoRecord(RecordBuilder):

    def __init__(self, sensor_id: int, packet: Dict[str, Any]):
        super(SensorInfoRecord, self).__init__(sensor_id)
        self.last_acquisition = packet.get('last_acquisition')
        self.channel = packet.get('channel')

        if not self.channel or not self.last_acquisition:
            raise SystemExit(f"{SensorInfoRecord.__name__}: bad packet => please check you packet has a non-empty list"
                             f"of channel name(s) and a non-empty list of last acquisition, one for each channel(s).")
        if len(self.channel) != len(self.last_acquisition):
            raise SystemExit(f"{SensorInfoRecord.__name__}: bad packet => number of channel(s) does not match the "
                             f"number of last acquisition value(s)")

    def record(self) -> str:
        records = ','.join(
            f"({self.sensor_id}, '{ch}', '{tsmp.ts}')" for ch, tsmp in zip(self.channel, self.last_acquisition))
        return records.strip(',')


class MobileMeasureRecord(RecordBuilder):

    def __init__(self, packet: Dict[str, Any]):
        super(MobileMeasureRecord, self).__init__(sensor_id=-1)
        self.measure_param_map = None
        self.record_id = packet['record_id']
        self.timestamp = packet['timestamp']
        self.geom = packet['geom']
        self.param_name = packet.get('param_name')
        self.param_val = packet.get('param_value')
        if not self.param_name or not self.param_val:
            raise SystemExit(
                f"{MobileMeasureRecord.__name__}: bad packet => please check you packet has a non-empty list"
                f"of param name(s) and a non-empty list of param value(s), one for each name(s).")
        if len(self.param_name) != len(self.param_val):
            raise SystemExit(f"{MobileMeasureRecord.__name__}: bad packet => number of param name(s) does not match the "
                             f"number of param value(s)")

    def set_measure_param_map(self, param_map: Dict[str, Any]):
        self.measure_param_map = param_map

    def record(self) -> str:

        if self.measure_param_map is None:
            raise SystemExit(f"{MobileMeasureRecord.__name__}: bad setup => missing external dependency 'measure_param_map'")

        records = ','.join(
            f"({self.record_id}, {self.measure_param_map[name]}, '{value}', '{self.timestamp.ts}', {self.geom})"
            for name, value in zip(self.param_name, self.param_val))
        return records.strip(',')


class StationMeasureRecord(RecordBuilder):

    def __init__(self, sensor_id: int, packet: Dict[str, Any]):
        super(StationMeasureRecord, self).__init__(sensor_id)
        self.measure_param_map = None
        self.record_id = packet['record_id']
        self.timestamp = packet['timestamp']
        self.param_name = packet.get('param_name')
        self.param_val = packet.get('param_value')
        if not self.param_name or not self.param_val:
            raise SystemExit(f"{StationMeasureRecord.__name__}: bad packet => please check you packet has a non-empty list"
                             f"of param name(s) and a non-empty list of param value(s), one for each name(s).")
        if len(self.param_name) != len(self.param_val):
            raise SystemExit(f"{StationMeasureRecord.__name__}: bad packet => number of param name(s) does not match the "
                             f"number of param value(s)")

    def set_measure_param_map(self, param_map: Dict[str, Any]):
        self.measure_param_map = param_map

    def record(self) -> str:

        if self.measure_param_map is None:
            raise SystemExit(f"{StationMeasureRecord.__name__}: bad setup => missing external dependency 'measure_param_map'")

        records = ','.join(
            f"({self.record_id}, {self.measure_param_map[name]}, {self.sensor_id}, '{value}', '{self.timestamp.ts}')"
            for name, value in zip(self.param_name, self.param_val))
        return records.strip(',')
