######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 05/11/21 17:37
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from abc import abstractmethod
from typing import Dict, Any, List
from airquality.container.filterable_container import FilterableContainer, ContainerFilter


class SQLContainer(FilterableContainer):
    """Interface to SQL containers object that can be translated into SQL query."""

    @abstractmethod
    def sql(self, query: str) -> str:
        pass

    def apply_filter(self, container_filter: ContainerFilter):
        return True


class GeoSQLContainer(SQLContainer):
    """SQL container that defines how a sensor location in translated into SQL query."""

    def __init__(self, sensor_id: int, packet: Dict[str, Any]):
        self.sensor_id = sensor_id
        self.timestamp = packet['timestamp']
        self.geometry = packet['geometry']

    def sql(self, query: str) -> str:
        return query + f"({self.sensor_id}, '{self.timestamp}', {self.geometry})"

    def __str__(self):
        return f"sensor_id={self.sensor_id}, valid_from={self.timestamp}, geom={self.geometry}"


class APIParamSQLContainer(SQLContainer):
    """SQL container that defines how the sensor's API parameter is translated into SQL query."""

    def __init__(self, sensor_id: int, packet: Dict[str, Any]):
        self.sensor_id = sensor_id
        self.param_name: List[str] = packet['param_name']      # this is a List
        self.param_value: List[str] = packet['param_value']    # this is a List

    def sql(self, query: str) -> str:
        for i in range(len(self.param_name)):
            query += f"({self.sensor_id}, '{self.param_name[i]}', '{self.param_value[i]}')"
        return query

    def __str__(self):
        s = f"sensor_id={self.sensor_id}, "
        s += ', '.join(f'{name}={val}' for name in self.param_name for val in self.param_value)
        return s


class SensorSQLContainer(SQLContainer):

    def __init__(self, sensor_id: int, packet: Dict[str, Any]):
        self.name = packet['name']
        self.type = packet['type']

    def sql(self, query: str) -> str:
        return query + f"('{self.type}', '{self.name}')"

    def apply_filter(self, container_filter: ContainerFilter):
        return container_filter.filter_container(to_filter=self.name)

    def __str__(self):
        return f"name={self.name}, type={self.type}"


########################### SQL CONTAINER COMPOSITION CLASS ############################
class SQLContainerComposition(SQLContainer):

    def __init__(self, containers: List[SQLContainer]):
        self.containers = containers

    def sql(self, query: str) -> str:
        for c in self.containers:
            query += c.sql(query="") + ','
        return query.strip(',') + ';'

    def apply_filter(self, container_filter: ContainerFilter):
        filtered_containers = []
        for c in self.containers:
            if c.apply_filter(container_filter=container_filter):
                filtered_containers.append(c)
        return filtered_containers

    def __str__(self):
        return ', '.join(f'{c!s}' for c in self.containers)
