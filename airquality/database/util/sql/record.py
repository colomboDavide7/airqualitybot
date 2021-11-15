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
        records = ','.join(f"({self.sensor_id}, '{ch}', '{tsmp.ts}')" for ch, tsmp in zip(self.channel, self.last_acquisition))
        return records.strip(',')


# class MobileMeasurementSQLContainer(SQLBuilder):
#
#     # TODO: ADD EXTERNAL MEASUREMENT ID
#
#     def __init__(self, packet: Dict[str, Any]):
#         self.param_id = packet['param_id']
#         self.param_val = packet['param_val']
#         self.timestamp = packet['timestamp']
#         self.geom = packet['geom']
#
#     def sql(self, query: str) -> str:
#         for i in range(len(self.param_id)):
#             value = self.param_val[i]
#             if value is not None:
#                 value = f"'{value}'"
#             query += f"({self.param_id[i]}, {value}, '{self.timestamp}', {self.geom}),"
#         return query.strip(',')
#
#     def __str__(self):
#         return ', '.join(f'{id_}={val}' for id_, val in zip(self.param_id, self.param_val))


# class StationMeasurementSQLContainer(SQLBuilder):
#
#     # TODO: ADD EXTERNAL MEASUREMENT ID
#
#     def __init__(self, sensor_id: int, packet: Dict[str, Any]):
#         self.sensor_id = sensor_id
#         self.param_id = packet['param_id']
#         self.param_val = packet['param_val']
#         self.timestamp = packet['timestamp']
#
#     def sql(self, query: str) -> str:
#         for i in range(len(self.param_id)):
#             value = self.param_val[i]
#             if value is not None:
#                 value = f"'{value}'"
#             query += f"({self.param_id[i]}, {self.sensor_id}, {value}, '{self.timestamp}'),"
#         return query.strip(',')
#
#     def __str__(self):
#         s = f"sensor_id={self.sensor_id}, "
#         s += ', '.join(f'{id_}={val}' for id_, val in zip(self.param_id, self.param_val))
#         return s
