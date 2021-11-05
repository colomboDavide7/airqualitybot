######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 05/11/21 17:48
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List
from abc import ABC, abstractmethod
from airquality.container.sql_container import SQLContainer, APIParamSQLContainer, GeoSQLContainer, SensorSQLContainer
from airquality.container.sql_container_composition import APIParamSQLContainerComposition
from airquality.container.filterable_container import FilterableContainer
from airquality.filter.container_filter import ContainerFilter


class InitializeSQLDispatcher(ABC):
    """SQL dispatcher class for the 'initialize' module that defines methods for api parameters, sensor and location
    dispatching from API to database."""

    @abstractmethod
    def api_param_sql(self, query: str) -> str:
        pass

    @abstractmethod
    def sensor_sql(self, query: str) -> str:
        pass

    @abstractmethod
    def geo_sql(self, query: str) -> str:
        pass


class InitializePacketSQLDispatcher(InitializeSQLDispatcher):
    """SQL dispatcher that implements the abstract interface for dispatching parameters in a single packet fetched from
    API and converting it into SQL query to be inserted into the database."""

    def __init__(self, containers: List[SQLContainer]):
        self.containers = containers

    def api_param_sql(self, query: str) -> str:
        for c in self.containers:
            if isinstance(c, APIParamSQLContainerComposition) or isinstance(c, APIParamSQLContainer):
                query += c.sql() + ','
        return query

    def sensor_sql(self, query: str) -> str:
        for c in self.containers:
            if isinstance(c, SensorSQLContainer):
                query += c.sql() + ','
        return query

    def geo_sql(self, query: str) -> str:
        for c in self.containers:
            if isinstance(c, GeoSQLContainer):
                query += c.sql() + ','
        return query


class InitializePacketSQLDispatcherComposition(InitializeSQLDispatcher):
    """SQL dispatcher composition object that holds a list of single packet dispatcher."""

    def __init__(self, packet_containers: List[InitializePacketSQLDispatcher]):
        self.packet_containers = packet_containers

    def api_param_sql(self, query: str) -> str:
        for c in self.packet_containers:
            query += c.api_param_sql(query="")
        return query.strip(',') + ';'

    def sensor_sql(self, query: str) -> str:
        for c in self.packet_containers:
            query += c.sensor_sql(query="")
        return query.strip(',') + ';'

    def geo_sql(self, query: str) -> str:
        for c in self.packet_containers:
            query += c.geo_sql(query="")
        return query.strip(',') + ';'
