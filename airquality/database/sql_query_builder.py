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
from airquality.app import EMPTY_STRING
from airquality.parser.file_parser import FileParserFactory
from airquality.picker import PARAM_ID, PARAM_VALUE, TIMESTAMP, GEOMETRY


class SQLQueryBuilder(builtins.object):
    """Class that builds dynamically the sql query to be sent to the database.

    The __init__() method takes the path to the query file."""


    def __init__(self, query_file_path: str):
        self.__path = query_file_path
        self.__raw = IOManager.open_read_close_file(self.__path)
        parser = FileParserFactory.file_parser_from_file_extension(file_extension = query_file_path.split('.')[-1])
        self.__parsed = parser.parse(self.__raw)


    def _raise_exception_if_query_identifier_not_found(self, query_id: str):
        if query_id not in self.__parsed.keys():
            raise SystemExit(f"{SQLQueryBuilder.__name__}: query id '{query_id}' not found. "
                             f"Please check your 'properties/sql_query.json' file.")


    def select_sensor_ids_from_identifier(self, identifier: str) -> str:

        query_id = "sensor_ids_from_identifier"
        self._raise_exception_if_query_identifier_not_found(query_id = query_id)
        return self.__parsed[query_id].format(identifier=identifier)


    def select_api_param_from_sensor_id(self, sensor_id: int) -> str:

        query_id = "api_param_from_sensor_id"
        self._raise_exception_if_query_identifier_not_found(query_id = query_id)
        return self.__parsed[query_id].format(id = sensor_id)


    def select_measure_param_from_identifier(self, identifier: str) -> str:

        query_id = "measure_param_from_identifier"
        self._raise_exception_if_query_identifier_not_found(query_id = query_id)
        return self.__parsed[query_id].format(identifier=identifier)


    def insert_atmotube_measurement_packets(self, packets: List[Dict[str, Any]]) -> str:
        """This method returns the query for inserting the Atmotube packets into the database.

        It takes a List of packets (i.e., a dictionary) built by the APIPacketPicker.

        If the packet list is empty, an EMPTY_STRING query is returned."""

        query_id = "insert_mobile_measurement"
        self._raise_exception_if_query_identifier_not_found(query_id = query_id)

        query = EMPTY_STRING
        if packets:
            query = self.__parsed[query_id]

            for packet in packets:
                query += f"({packet[PARAM_ID]}, " \
                         f"{packet[PARAM_VALUE]}, " \
                         f"{packet[TIMESTAMP]}, " \
                         f"{packet[GEOMETRY]}),"

            query = query.strip(',') + ';'
        return query


    def update_last_packet_date_atmotube(self, last_timestamp: str, sensor_id: int) -> str:
        """This method returns a query for updating the last acquisition timestamp of an atmotube sensor, in order
        to let the bot knows the next time it runs from where to start in fetching data from API and for loading
        into the database without redundancy.

        If an EMPTY_STRING timestamp is passed as argument, an EMPTY_STRING query is returned.
        """

        query_id = "update_last_packet_date_atmotube"
        self._raise_exception_if_query_identifier_not_found(query_id = query_id)

        query = EMPTY_STRING
        if last_timestamp != EMPTY_STRING:
            query = self.__parsed[f"{query_id}"].format(par_val = last_timestamp, sens_id = sensor_id, par_name = "date")
        return query


    def insert_manufacturer(self, personality: str) -> str:
        """This method builds the query for inserting a new manufacturer record into the database by using the
        'personality' argument."""

        query_id = "insert_manufacturer"
        self._raise_exception_if_query_identifier_not_found(query_id = query_id)

        query = EMPTY_STRING
        if personality == "purpleair":
            query = self.__parsed[query_id].format(name="'PurpleAir Inc.'", model = "'PurpleAir PA-II'")
        return query

    def select_max_manufacturer_id(self) -> str:
        """This method returns a query for selecting the manufacturer id associated to the 'identifier' argument.

        The identifier is searched into the model name."""

        query_id = "select_max_manufacturer_id"
        self._raise_exception_if_query_identifier_not_found(query_id = query_id)

        return self.__parsed[query_id]

    def select_max_sensor_id(self) -> str:

        query_id = "select_max_sensor_id"
        self._raise_exception_if_query_identifier_not_found(query_id = query_id)

        return self.__parsed[query_id]
