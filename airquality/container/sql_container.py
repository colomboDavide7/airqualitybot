######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 05/11/21 17:37
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from abc import ABC, abstractmethod


class SQLContainer(ABC):
    """Interface to SQL containers object that can be translated into SQL query."""

    @abstractmethod
    def sql(self) -> str:
        pass


class GeoSQLContainer(SQLContainer):
    """SQL container that defines how a sensor location in translated into SQL query."""

    def __init__(self, sensor_id, timestamp, geometry):
        self.sensor_id = sensor_id
        self.timestamp = timestamp
        self.geometry = geometry

    def sql(self) -> str:
        return f"({self.sensor_id}, '{self.timestamp}', {self.geometry})"


class APIParamSQLContainer(SQLContainer):
    """SQL container that defines how the sensor's API parameter is translated into SQL query."""

    def __init__(self, param_name, param_value, sensor_id):
        self.param_name = param_name
        self.param_value = param_value
        self.sensor_id = sensor_id

    def sql(self) -> str:
        return f"({self.sensor_id}, '{self.param_name}', '{self.param_value}')"


class SensorSQLContainer(SQLContainer):

    def __init__(self, sensor_name, sensor_type):
        self.name = sensor_name
        self.type = sensor_type

    def sql(self) -> str:
        return f"('{self.type}', '{self.name}')"
