#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 10:29
# @Description: this script defines a class for dynamically build valid sql queries.
#
#################################################
import builtins
from typing import Dict, Any, List
from airquality.io.io import IOManager
from airquality.parser.file_parser import FileParserFactory
from airquality.picker.api_packet_picker import APIPacketPicket


class SQLQueryBuilder(builtins.object):
    """Class that builds dynamically the sql query to be sent to the database.

    The __init__() method takes the path to the query file."""


    def __init__(self, query_file_path: str):
        self.__path = query_file_path
        self.__raw = IOManager.open_read_close_file(self.__path)
        parser = FileParserFactory.file_parser_from_file_extension(file_extension = query_file_path.split('.')[-1])
        self.__parsed = parser.parse(self.__raw)


    def select_sensor_ids_from_identifier(self, identifier: str) -> str:
        """This method returns a string that contains sql query for selecting

        If 'identifier' is empty, SystemExit exception is raised.

        If 'query_id' does not match one of the sql query identifier in 'properties/sql_query.json' file,
        SystemExit exception is raised."""

        query_id = "sensor_ids_from_identifier"

        if query_id not in self.__parsed.keys():
            raise SystemExit(f"{SQLQueryBuilder.__name__}: query id '{query_id}' not found in method "
                             f"'{SQLQueryBuilder.select_sensor_ids_from_identifier.__name__}()'. "
                             f"Please check your 'properties/sql_query.json' file.")

        return self.__parsed[query_id].format(identifier=identifier)


    def select_api_param_from_sensor_id(self, sensor_id: int) -> str:

        query_id = "api_param_from_sensor_id"

        if query_id not in self.__parsed.keys():
            raise SystemExit(f"{SQLQueryBuilder.__name__}: query id '{query_id}' not found in method "
                             f"'{SQLQueryBuilder.select_api_param_from_sensor_id.__name__}()'. "
                             f"Please check your 'properties/sql_query.json' file.")

        return self.__parsed[query_id].format(id = sensor_id)


    def select_measure_param_from_identifier(self, identifier: str) -> str:

        query_id = "measure_param_from_identifier"

        if query_id not in self.__parsed.keys():
            raise SystemExit(f"{SQLQueryBuilder.__name__}: query id '{query_id}' not found in method "
                             f"'{SQLQueryBuilder.select_api_param_from_sensor_id.__name__}()'. "
                             f"Please check your 'properties/sql_query.json' file.")

        return self.__parsed[query_id].format(identifier=identifier)


    def insert_measurement(self, packets: List[Dict[str, Any]]) -> str:

        query_id = "insert_mobile_measurement"

        if query_id not in self.__parsed.keys():
            raise SystemExit(f"{SQLQueryBuilder.__name__}: query id '{query_id}' not found in method "
                             f"'{SQLQueryBuilder.insert_measurement.__name__}()'. "
                             f"Please check your 'properties/sql_query.json' file.")

        query = self.__parsed[query_id]

        for packet in packets:
            query += f"({packet[APIPacketPicket.PARAM_ID]}, " \
                     f"{packet[APIPacketPicket.PARAM_VALUE]}, " \
                     f"{packet[APIPacketPicket.TIMESTAMP]}, " \
                     f"{packet[APIPacketPicket.GEOMETRY]}),"

        query = query.strip(',') + ';'
        return query
