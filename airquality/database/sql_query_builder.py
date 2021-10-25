#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 10:29
# @Description: this script defines a class for dynamically build valid sql queries.
#
#################################################
import builtins

from typing import Dict, Any, List
from airquality.constants.shared_constants import EMPTY_STRING, \
    PICKER2SQLBUILDER_PARAM_ID, PICKER2SQLBUILDER_PARAM_VAL, \
    PICKER2SQLBUILDER_TIMESTAMP, PICKER2SQLBUILDER_GEOMETRY


from airquality.io.io import IOManager
from airquality.parser.file_parser import FileParserFactory
from airquality.parser.datetime_parser import DatetimeParser
from airquality.picker.api_packet_picker import APIPacketPicker


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
        """This method returns a SQL query that selects all the "sensor_id"(s) from the database, which "sensor_type"
        contains the identifier argument."""

        query_id = "sensor_ids_from_identifier"
        self._raise_exception_if_query_identifier_not_found(query_id = query_id)
        return self.__parsed[query_id].format(identifier=identifier)


    def select_api_param_from_sensor_id(self, sensor_id: int) -> str:
        """This method return a query for selecting 'param_name, param_value' tuples associated to a given "sensor_id"."""

        query_id = "api_param_from_sensor_id"
        self._raise_exception_if_query_identifier_not_found(query_id = query_id)
        return self.__parsed[query_id].format(id = sensor_id)


    def select_measure_param_from_identifier(self, identifier: str) -> str:
        """This method returns a query for selecting 'param_code, id' tuples which 'param_name' contains the identifier
        argument."""

        query_id = "measure_param_from_identifier"
        self._raise_exception_if_query_identifier_not_found(query_id = query_id)
        return self.__parsed[query_id].format(identifier=identifier)


    def insert_atmotube_measurement_packets(self, packets: List[Dict[str, Any]]) -> str:
        """This method returns the query for inserting the Atmotube packets into the database.

        It takes a List of packets (i.e., a dictionary) built by the APIPacketPicker.

        If the packet list is empty, an 'EMPTY_STRING' value is returned."""

        query_id = "insert_mobile_measurement"
        self._raise_exception_if_query_identifier_not_found(query_id = query_id)

        query = EMPTY_STRING
        if packets:
            query = self.__parsed[query_id]

            for packet in packets:
                query += f"({packet[PICKER2SQLBUILDER_PARAM_ID]}, " \
                         f"{packet[PICKER2SQLBUILDER_PARAM_VAL]}, " \
                         f"{packet[PICKER2SQLBUILDER_TIMESTAMP]}, " \
                         f"{packet[PICKER2SQLBUILDER_GEOMETRY]}),"

            query = query.strip(',') + ';'
        return query


    def update_last_packet_date_atmotube(self, last_timestamp: str, sensor_id: int) -> str:
        """This method returns a query for updating the last acquisition timestamp of an atmotube sensor, in order
        to let the bot knows the next time it runs from where to start fetching data from API and loading them
        into the database without redundancy.

        If an EMPTY_STRING timestamp is passed as argument, an EMPTY_STRING query is returned."""

        query_id = "update_last_packet_date_atmotube"
        self._raise_exception_if_query_identifier_not_found(query_id = query_id)

        query = EMPTY_STRING
        if last_timestamp != EMPTY_STRING:
            query = self.__parsed[f"{query_id}"].format(par_val = last_timestamp, sens_id = sensor_id, par_name = "date")
        return query


    def select_max_sensor_id(self) -> str:
        """This method returns a query for selecting the MAX 'sensor_id' from sensor table."""

        query_id = "select_max_sensor_id"
        self._raise_exception_if_query_identifier_not_found(query_id = query_id)
        return self.__parsed[query_id]


    def select_all_sensor_name_from_identifier(self, identifier: str) -> str:
        """This method returns a query for selecting all the 'sensor_name' of records that contain the 'identifier'
        argument in the name."""

        query_id = "sensor_name_from_identifier"
        self._raise_exception_if_query_identifier_not_found(query_id = query_id)
        return self.__parsed[query_id].format(identifier = identifier)


    def insert_sensors_from_identifier(self, packets: List[Dict[str, Any]], identifier: str) -> str:
        """This method returns a query for inserting the 'sensor_type, sensor_name' tuples into the sensor table.

        The role of the 'identifier' argument is to both assemble the correct name and defining the 'sensor_type'."""

        query_id = "insert_sensors"
        self._raise_exception_if_query_identifier_not_found(query_id = query_id)
        query = EMPTY_STRING

        if packets:
            query = self.__parsed[query_id]
            for packet in packets:
                sensor_name = APIPacketPicker.pick_sensor_name_from_identifier(packet = packet, identifier = identifier)
                query += f"('{identifier}', '{sensor_name}'),"
            query = query.strip(',') + ';'
        return query


    def insert_api_param_from_identifier(self, packets: List[Dict[str, Any]], identifier: str, first_sensor_id: int) -> str:
        """This method returns a query for inserting the 'sensor_id, param_name, param_value' tuples in the api param
        table. If 'packets' argument is empty, 'EMPTY_STRING' values is returned.

        The argument 'first_sensor_id' is used as foreign key for the api param table. The value is increased by one
        every packet."""

        query_id = "insert_api_param"
        self._raise_exception_if_query_identifier_not_found(query_id = query_id)
        query = EMPTY_STRING

        if packets:
            query = self.__parsed[query_id]
            for packet in packets:
                api_param = APIPacketPicker.pick_api_param_from_packet(packet, identifier)
                for key, val in api_param.items():
                    query += f"({first_sensor_id}, '{key}', '{val}'),"
                first_sensor_id += 1
            query = query.strip(',') + ';'
        return query


    def insert_sensor_at_location(self, packets: List[Dict[str, Any]], identifier: str, first_sensor_id: int) -> str:
        """This method returns a query for inserting the 'sensor_id, valid_from, geom' tuples into the sensor at location
        table. If 'packets' argument is empty, 'EMPTY_STRING' values is returned.

        The argument 'first_sensor_id' is used as foreign key for the api param table. The value is increased by one
        every packet."""

        query_id = "insert_sensor_at_location"
        self._raise_exception_if_query_identifier_not_found(query_id = query_id)
        query = EMPTY_STRING

        if packets:
            query = self.__parsed[query_id]
            for packet in packets:
                geom = APIPacketPicker.pick_geometry_from_packet(packet = packet, identifier = identifier)
                timestamp = DatetimeParser.current_sqltimestamp()
                query += f"({first_sensor_id}, '{timestamp}', {geom}),"
                first_sensor_id += 1
            query = query.strip(',') + ';'
        return query
