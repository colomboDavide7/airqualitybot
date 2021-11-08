#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 10:29
# @Description: this script defines a class for dynamically build valid sql queries. The query are read from the
#               'properties/sql_query.json' file.
#
#################################################
import builtins
from typing import Dict, Any
from airquality.constants.shared_constants import EXCEPTION_HEADER


class QueryPicker(builtins.object):

    def __init__(self, parsed_query_data: Dict[str, Any]):
        if not parsed_query_data:
            raise SystemExit(f"{EXCEPTION_HEADER} cannot instantiate '{QueryPicker.__name__}' with empty dictionary.")
        self.parsed_query_data = parsed_query_data

    ################################ METHODS THAT RETURN SELECT QUERY ################################

    def select_max_sensor_id(self) -> str:
        """This method returns a query for selecting the MAX 'sensor_id' from sensor table."""

        query_id = "s1"
        self._raise_exception_if_query_identifier_not_found(query_id=query_id)
        return self.parsed_query_data[query_id]

    def select_api_param_from_sensor_id(self) -> str:
        """This method return a query for selecting 'param_name, param_value' tuples associated to a given "sensor_id"."""

        query_id = "s2"
        self._raise_exception_if_query_identifier_not_found(query_id=query_id)
        return self.parsed_query_data[query_id]

    def select_sensor_ids_from_personality(self, personality: str) -> str:
        """This method returns a SQL query that selects all the "sensor_id"(s) from the database, which "sensor_type"
        contains the identifier argument."""

        query_id = "s3"
        self._raise_exception_if_query_identifier_not_found(query_id=query_id)
        return self.parsed_query_data[query_id].format(personality=personality)

    def select_sensor_name_from_personality(self, personality: str) -> str:
        """This method returns a query for selecting all the records which 'sensor_name' field contains the 'identifier'
        argument."""

        query_id = "s4"
        self._raise_exception_if_query_identifier_not_found(query_id=query_id)
        return self.parsed_query_data[query_id].format(personality=personality)

    def select_measure_param_from_personality(self, personality: str) -> str:
        """This method returns a query for selecting 'param_code, id' tuples which 'param_name' contains the identifier
        argument."""

        query_id = "s5"
        self._raise_exception_if_query_identifier_not_found(query_id=query_id)
        return self.parsed_query_data[query_id].format(personality=personality)

    def select_sensor_valid_name_geom_mapping_from_personality(self, personality: str) -> str:
        query_id = "s6"
        self._raise_exception_if_query_identifier_not_found(query_id=query_id)
        return self.parsed_query_data[query_id].format(personality=personality)

    def select_sensor_name_id_mapping_from_personality(self, personality: str) -> str:
        query_id = "s7"
        self._raise_exception_if_query_identifier_not_found(query_id)
        return self.parsed_query_data[query_id].format(personality=personality)

    ################################ METHODS THAT RETURN INSERT QUERY ################################

    def insert_into_mobile_measurements(self) -> str:
        query_id = "i1"
        self._raise_exception_if_query_identifier_not_found(query_id=query_id)
        return self.parsed_query_data[query_id]

    def insert_into_station_measurements(self) -> str:
        query_id = "i2"
        self._raise_exception_if_query_identifier_not_found(query_id)
        return self.parsed_query_data[query_id]

    def insert_into_sensor(self) -> str:
        query_id = "i3"
        self._raise_exception_if_query_identifier_not_found(query_id=query_id)
        return self.parsed_query_data[query_id]

    def insert_into_api_param(self) -> str:
        query_id = "i4"
        self._raise_exception_if_query_identifier_not_found(query_id=query_id)
        return self.parsed_query_data[query_id]

    def insert_into_sensor_at_location(self) -> str:
        query_id = "i5"
        self._raise_exception_if_query_identifier_not_found(query_id=query_id)
        return self.parsed_query_data[query_id]

    ################################ METHODS THAT RETURN UPDATE QUERY ################################

    def update_last_packet_date_atmotube(self, last_timestamp: str, sensor_id: int) -> str:
        """This method returns a query for updating the last acquisition timestamp of an atmotube sensor, in order
        to let the bot knows the next time it runs from where to start fetching data from API and loading them
        into the database without redundancy.

        If an EMPTY_STRING timestamp is passed as argument, an EMPTY_STRING query is returned."""

        query_id = "u1"
        self._raise_exception_if_query_identifier_not_found(query_id=query_id)
        query = self.parsed_query_data[f"{query_id}"].format(par_val=last_timestamp, sens_id=sensor_id, par_name="date")
        return query

    def update_valid_to_timestamp_location(self) -> str:

        query_id = "u2"
        self._raise_exception_if_query_identifier_not_found(query_id)
        return self.parsed_query_data[query_id]

    def update_last_channel_acquisition_timestamp(self, sensor_id: str, ts: str, param2update: str) -> str:

        query_id = "u3"
        self._raise_exception_if_query_identifier_not_found(query_id)
        return self.parsed_query_data[query_id].format(ts=ts, sens_id=sensor_id, par_name=param2update)

    ################################ EXCEPTION METHOD ################################

    def _raise_exception_if_query_identifier_not_found(self, query_id: str):
        """This method raises SystemExit exception is the 'query_id' argument is not present within the query
        identifiers read from the SQL FILE passed to '__init__()' method."""

        if query_id not in self.parsed_query_data.keys():
            raise SystemExit(f"{EXCEPTION_HEADER} {QueryPicker.__name__} is missing query_id='{query_id}'.")
