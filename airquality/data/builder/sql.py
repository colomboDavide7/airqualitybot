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
from airquality.core.constants.shared_constants import EXCEPTION_HEADER


class SQLBuilder(abc.ABC):

    def __init__(self, sensor_id: int):
        self.sensor_id = sensor_id

    @abc.abstractmethod
    def sql(self) -> str:
        pass


class SensorAtLocationSQLBuilder(SQLBuilder):

    def __init__(self, sensor_id: int, valid_from: str, geom: str):
        super().__init__(sensor_id)
        self.valid_from = valid_from
        self.geom = geom

    def sql(self) -> str:
        return f"({self.sensor_id}, '{self.valid_from}', {self.geom})"

    def __str__(self):
        return f"sensor_id={self.sensor_id}, valid_from={self.valid_from}, geom={self.geom}"


class APIParamSQLBuilder(SQLBuilder):

    def __init__(self, sensor_id: int, packet: Dict[str, Any]):
        super().__init__(sensor_id)
        try:
            self.param_name = packet['param_name']
            self.param_value = packet['param_value']
        except KeyError as ke:
            raise SystemExit(f"{EXCEPTION_HEADER}{APIParamSQLBuilder.__name__} bad parameters => missing key={ke!s}.")

    def sql(self) -> str:
        values = ""
        for i in range(len(self.param_name)):
            values += f"({self.sensor_id}, '{self.param_name[i]}', '{self.param_value[i]}'),"
        return values.strip(',')

    def __str__(self):
        s = f"sensor_id={self.sensor_id}, "
        s += ', '.join(f'{name}={val}' for name, val in zip(self.param_name, self.param_value))
        return s


class SensorSQLBuilder(SQLBuilder):

    def __init__(self, sensor_id: int, packet: Dict[str, Any]):
        super().__init__(sensor_id)
        try:
            self.sensor_name = packet['name']
            self.sensor_type = packet['type']
        except KeyError as ke:
            raise SystemExit(f"{EXCEPTION_HEADER}{APIParamSQLBuilder.__name__} bad parameters => missing key={ke!s}.")

    def sql(self) -> str:
        return f"('{self.sensor_type}', '{self.sensor_name}')"

    def __str__(self):
        return f"name={self.sensor_name}, type={self.sensor_type}"


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


########################### SQL CONTAINER COMPOSITION CLASS ############################
# class SQLCompositionBuilder(SQLBuilder):
#
#     def __init__(self, sensor_id: int, containers: List[SQLBuilder]):
#         super().__init__(sensor_id)
#         self.containers = containers
#
#     def sql(self, query: str) -> str:
#         for c in self.containers:
#             query += c.sql(query="") + ','
#         return query.strip(',') + ';'
#
#     def __str__(self):
#         return '\n'.join(f'{c!s}' for c in self.containers)
