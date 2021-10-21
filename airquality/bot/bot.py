#################################################
#
# @Author: davidecolombo
# @Date: mar, 19-10-2021, 19:11
# @Description: This module contains the BaseBot class and its subclasses
#
#################################################
from abc import ABC
from typing import List
from airquality.conn.builder import SQLQueryBuilder
from airquality.conn.conn import Psycopg2ConnectionAdapter
from airquality.parser.db_resp_parser import DatabaseResponseParser


class BaseBot(ABC):
    """
    Abstract Base Class for bot objects.

    -db_conn_interface: instance of Psycopg2ConnectionAdapter
    -query_builder:     instance of SQLQueryBuilder class
    """

    def __init__(self, dbconn: Psycopg2ConnectionAdapter, query_builder: SQLQueryBuilder):
        self.__db_conn_interface = dbconn
        self.__db_conn_interface.open_conn()
        self.__query_builder = query_builder

    @property
    def dbconn(self):
        return self.__db_conn_interface

    @property
    def sqlbuilder(self):
        return self.__query_builder



class BotMobile(BaseBot):
    """
    Subclass of BaseBot that handles mobile sensors data automatically.

    The purpose of this class is to fetch data through the sensor's API and
    loading the data to the database.
    """

    def __init__(self,
                 dbconn: Psycopg2ConnectionAdapter,
                 query_builder: SQLQueryBuilder,
                 sensor_models: List[str]
                 ):
        super().__init__(dbconn, query_builder)
        self.__models = sensor_models
        query = self.sqlbuilder.select_mobile_sensor_ids(self.__models)
        response = self.dbconn.send(query)
        sensor_ids = DatabaseResponseParser.parse_one_field_response(response)
        if not sensor_ids:
            raise SystemExit(f"{BotMobile.__name__}: sensor id list is empty in method '{BotMobile.__init__.__name__}()'. "
                             f"Please, check your 'properties/resources.json' file.")
        self.__sensor_ids = sensor_ids
