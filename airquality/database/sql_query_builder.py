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
from airquality.parser.datetime_parser import DatetimeParser
from airquality.picker.resource_picker import ResourcePicker
from airquality.geom.postgis_geom_builder import PostGISGeomBuilder
from airquality.constants.shared_constants import EMPTY_STRING, EMPTY_LIST, \
    RESHAPER2SQLBUILDER_PARAM_ID, RESHAPER2SQLBUILDER_PARAM_VAL, \
    RESHAPER2SQLBUILDER_TIMESTAMP, RESHAPER2SQLBUILDER_GEOMETRY, RESHAPER2SQLBUILDER_SENSOR_ID, \
    GEO_TYPE_ST_POINT_2D


class SQLQueryBuilder(builtins.object):
    """Class that builds dynamically the sql query to be sent to the database.

    The __init__() method takes the path to the query file, then opens, reads and closes the file.
    Next, the parsed content is stored in an instance variable."""


    def __init__(self, query_file_path: str):
        self.__path = query_file_path
        self.__raw = IOManager.open_read_close_file(self.__path)
        parser = FileParserFactory.file_parser_from_file_extension(file_extension = query_file_path.split('.')[-1])
        self.__parsed = parser.parse(self.__raw)


################################ METHODS THAT RETURN SELECT QUERY ################################


    def select_sensor_ids_from_identifier(self, identifier: str) -> str:
        """This method returns a SQL query that selects all the "sensor_id"(s) from the database, which "sensor_type"
        contains the identifier argument."""

        query_id = "sensor_ids_from_identifier"
        self._raise_exception_if_query_identifier_not_found(query_id = query_id)
        return self.__parsed[query_id].format(identifier=identifier)


    def select_sensor_api_param(self, sensor_id: int) -> str:
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


    def select_max_sensor_id(self) -> str:
        """This method returns a query for selecting the MAX 'sensor_id' from sensor table."""

        query_id = "select_max_sensor_id"
        self._raise_exception_if_query_identifier_not_found(query_id = query_id)
        return self.__parsed[query_id]


    def select_all_sensor_name_from_identifier(self, identifier: str) -> str:
        """This method returns a query for selecting all the records which 'sensor_name' field contains the 'identifier'
        argument."""

        query_id = "sensor_name_from_identifier"
        self._raise_exception_if_query_identifier_not_found(query_id = query_id)
        return self.__parsed[query_id].format(identifier = identifier)


    def select_last_acquisition_timestamp_from_station_id(self, station_id: int):
        """This method returns a query for selecting the most recent timestamp associated with the given 'station_id'
        from the 'station_measurement' table. (valid for thingspeak and purpleair)."""

        query_id = "select_last_acquisition_timestamp_from_station_id"
        self._raise_exception_if_query_identifier_not_found(query_id = query_id)
        return self.__parsed[query_id].format(sens_id = station_id)


    def select_sensor_at_active_location_from_identifier(self, identifier: str) -> str:
        """This method returns a query that selects the (sensor_id, ST_AsText(geom)) tuple from the sensor_at_location
        table by looking only at those sensors whose type contains the identifiers and whose 'valid_to' field is NULL."""

        query_id = "select_sensor_at_location_from_identifier"
        self._raise_exception_if_query_identifier_not_found(query_id = query_id)
        return self.__parsed[query_id].format(identifier = identifier)


    def select_sensor_name_id_map_from_identifier(self, identifier: str) -> str:
        """This method returns a query that selects the (sensor_name, sensor_id) tuples that correspond to the
         identifier argument."""

        query_id = "sensor_name_id_map_from_identifier"
        self._raise_exception_if_query_identifier_not_found(query_id)
        return self.__parsed[query_id].format(identifier = identifier)


################################ METHODS THAT RETURN INSERT QUERY ################################


    def insert_atmotube_measurements(self, packets: List[Dict[str, Any]]) -> str:
        """This method returns the query for inserting the Atmotube packets into the database.

        Each item of the 'packets' list is a dictionary of the form:
            - param_id:     id of the measure param taken from the database
            - param_val:    value of the measure param taken from the packet downloaded from the API
            - timestamp:    packet timestamp taken from the API
            - geom:         string for building geometry object or null if 'coords' is missing

        If the packet list is empty, an 'EMPTY_STRING' value is returned."""

        query_id = "insert_mobile_measurement"
        self._raise_exception_if_query_identifier_not_found(query_id = query_id)

        query = ""
        if packets != EMPTY_LIST:
            query = self.__parsed[query_id]
            for packet in packets:
                query += f"({packet[RESHAPER2SQLBUILDER_PARAM_ID]}, " \
                         f"{packet[RESHAPER2SQLBUILDER_PARAM_VAL]}, " \
                         f"{packet[RESHAPER2SQLBUILDER_TIMESTAMP]}, " \
                         f"{packet[RESHAPER2SQLBUILDER_GEOMETRY]}),"

            query = query.strip(',') + ';'
        return query


    def insert_station_measurements(self, packets: List[Dict[str, Any]]) -> str:

        query_id = "insert_station_measurements"
        self._raise_exception_if_query_identifier_not_found(query_id)

        query = ""
        if packets == EMPTY_LIST:
            return query

        query = self.__parsed[query_id]
        for packet in packets:
            query += f"({packet[RESHAPER2SQLBUILDER_PARAM_ID]}, " \
                     f"{packet[RESHAPER2SQLBUILDER_SENSOR_ID]}, " \
                     f"{packet[RESHAPER2SQLBUILDER_PARAM_VAL]}," \
                     f"{packet[RESHAPER2SQLBUILDER_TIMESTAMP]}),"

        query = query.strip(',') + ';'
        return query



    def insert_sensors_from_identifier(self, packets: List[Dict[str, Any]], identifier: str) -> str:
        """This method returns a query for inserting the 'sensor_type, sensor_name' tuples into the sensor table.

        The role of the 'identifier' argument is to both assemble the correct name and defining the 'sensor_type'."""

        query_id = "insert_sensors"
        self._raise_exception_if_query_identifier_not_found(query_id = query_id)
        query = ""
        if packets == EMPTY_LIST:
            return query

        query = self.__parsed[query_id]
        for packet in packets:
            sensor_name = ResourcePicker.pick_sensor_name_from_identifier(packet = packet, personality = identifier)
            query += f"('{identifier}', '{sensor_name}'),"
        return query.strip(',') + ';'


    def insert_api_param(self, packets: List[Dict[str, Any]], first_sensor_id: int) -> str:
        """This method returns a query for inserting the 'sensor_id, param_name, param_value' tuples in the api param
        table. If 'packets' argument is empty, 'EMPTY_STRING' values is returned.

        The argument 'first_sensor_id' is used as foreign key for the api param table. The value is increased by one
        every packet."""

        query_id = "insert_api_param"
        self._raise_exception_if_query_identifier_not_found(query_id = query_id)
        query = ""
        if packets == EMPTY_LIST:
            return query

        query = self.__parsed[query_id]
        for packet in packets:
            for key, val in packet.items():
                query += f"({first_sensor_id}, '{key}', "
                if val is None:
                    query += f"null),"
                else:
                    query += f"'{val}'),"

            first_sensor_id += 1
        return query.strip(',') + ';'


    def insert_sensor_at_location(self, packets: List[Dict[str, Any]], first_sensor_id: int) -> str:
        """This method returns a query for inserting the 'sensor_id, valid_from, geom' tuples into the sensor at location
        table. If 'packets' argument is empty, 'EMPTY_STRING' values is returned.

        The argument 'first_sensor_id' is used as foreign key for the api param table. The value is increased by one
        every packet."""

        query_id = "insert_sensor_at_location"
        self._raise_exception_if_query_identifier_not_found(query_id = query_id)
        query = ""
        if packets == EMPTY_LIST:
            return query

        query = self.__parsed[query_id]
        for packet in packets:
            geom = PostGISGeomBuilder.build_geometry_type(geo_param = packet, geo_type = GEO_TYPE_ST_POINT_2D)
            timestamp = DatetimeParser.current_sqltimestamp()
            query += f"({first_sensor_id}, '{timestamp}', {geom}),"
            first_sensor_id += 1
        return query.strip(',') + ';'


    def insert_sensor_at_location_from_sensor_id(self, sensor_id: str, geom: str) -> str:

        query_id = "insert_sensor_at_location"
        self._raise_exception_if_query_identifier_not_found(query_id)
        query = self.__parsed[query_id]
        ts = DatetimeParser.current_sqltimestamp()
        query += f"({sensor_id}, '{ts}', {geom});"
        return query


################################ METHODS THAT RETURN UPDATE QUERY ################################


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


    def update_valid_to_timestamp_location(self, sensor_id: str) -> str:

        query_id = "update_valid_to_timestamp_location"
        self._raise_exception_if_query_identifier_not_found(query_id)
        ts = DatetimeParser.current_sqltimestamp()
        return self.__parsed[query_id].format(ts = ts, sens_id = sensor_id)


    def update_last_channel_acquisition_timestamp(self, sensor_id: str, ts: str, param2update: str) -> str:

        query_id = "update_last_channel_acquisition_timestamp"
        self._raise_exception_if_query_identifier_not_found(query_id)
        return self.__parsed[query_id].format(ts = ts, sens_id = sensor_id, par_name = param2update)



################################ EXCEPTION METHOD ################################


    def _raise_exception_if_query_identifier_not_found(self, query_id: str):
        """This method raises SystemExit exception is the 'query_id' argument is not present within the query
        identifiers read from the SQL FILE passed to '__init__()' method."""

        if query_id not in self.__parsed.keys():
            raise SystemExit(f"{SQLQueryBuilder.__name__}: query id '{query_id}' not found. "
                             f"Please check your 'properties/sql_query.json' file.")
