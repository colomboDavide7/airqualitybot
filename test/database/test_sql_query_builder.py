#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 10:32
# @Description: unit test script
#
#################################################
import unittest
from airquality.database.sql_query_builder import SQLQueryBuilder
from airquality.constants.shared_constants import EMPTY_STRING, EMPTY_LIST, \
    RESHAPER2SQLBUILDER_PARAM_ID, RESHAPER2SQLBUILDER_PARAM_VAL, RESHAPER2SQLBUILDER_TIMESTAMP, \
    RESHAPER2SQLBUILDER_GEOMETRY


class TestSQLQueryBuilder(unittest.TestCase):

    def setUp(self) -> None:
        """This method is run every time before a test is run."""
        self.sql_builder = SQLQueryBuilder(query_file_path="properties/sql_query.json")

    def test_system_exit_when_query_identifier_not_found(self):
        test_query_id = "bad query identifier"
        with self.assertRaises(SystemExit):
            self.sql_builder._raise_exception_if_query_identifier_not_found(query_id=test_query_id)

    def test_successfully_insert_atmotube_measurements(self):
        test_packets = [{RESHAPER2SQLBUILDER_PARAM_ID: "1",
                         RESHAPER2SQLBUILDER_PARAM_VAL: "'55.0'",
                         RESHAPER2SQLBUILDER_TIMESTAMP: "'2021-09-12 08:34:00'",
                         RESHAPER2SQLBUILDER_GEOMETRY: "null"}]

        expected_output = "INSERT INTO level0_raw.mobile_measurement (param_id, param_value, timestamp, geom) VALUES "
        expected_output += "(1, '55.0', '2021-09-12 08:34:00', null);"

        actual_output = self.sql_builder.insert_atmotube_measurements(packets=test_packets)
        self.assertEqual(actual_output, expected_output)

    def test_empty_query_when_empty_packet_list_insert_atmotube_measurement(self):
        """This method test the return value of 'EMPTY_STRING' when an EMPTY_LIST is passed as argument."""

        test_packets = EMPTY_LIST
        expected_output = EMPTY_STRING
        actual_output = self.sql_builder.insert_atmotube_measurements(packets=test_packets)
        self.assertEqual(actual_output, expected_output)

    def test_empty_query_when_empty_timestamp_update_last_date_atmotube(self):
        """This method test the return value of 'EMPTY_STRING' when an EMPTY_STRING is passed as argument."""

        test_timestamp = EMPTY_STRING
        expected_output = EMPTY_STRING
        actual_output = self.sql_builder.update_last_packet_date_atmotube(last_timestamp=test_timestamp,
                                                                          sensor_id=1)
        self.assertEqual(actual_output, expected_output)

    def test_successfully_insert_sensors(self):
        test_packets = [{"name": "n1", "sensor_index": "idx1"}]
        expected_output = "INSERT INTO level0_raw.sensor (sensor_type, sensor_name) VALUES "
        expected_output += "('purpleair', 'n1 (idx1)');"

        actual_output = self.sql_builder.insert_sensors_from_identifier(packets=test_packets, identifier="purpleair")
        self.assertEqual(actual_output, expected_output)

    def test_empty_query_if_empty_packet_list_when_insert_sensor(self):
        """This method test the return value of 'EMPTY_STRING' when an EMPTY_LIST is passed as argument."""

        expected_output = EMPTY_STRING
        actual_output = self.sql_builder.insert_sensors_from_identifier(packets=EMPTY_LIST, identifier="purpleair")
        self.assertEqual(actual_output, expected_output)

    def test_successfully_insert_api_param(self):
        test_packets = [{"par1": "val1", "par2": "val2"},
                        {"par1": "val3", "par2": "val4"}]
        test_first_sensor_id = 14

        expected_output = "INSERT INTO level0_raw.api_param (sensor_id, param_name, param_value) VALUES "
        expected_output += "(14, 'par1', 'val1'),"
        expected_output += "(14, 'par2', 'val2'),"
        expected_output += "(15, 'par1', 'val3'),"
        expected_output += "(15, 'par2', 'val4');"

        actual_output = self.sql_builder.insert_api_param(packets=test_packets, first_sensor_id=test_first_sensor_id)
        self.assertEqual(actual_output, expected_output)


if __name__ == '__main__':
    unittest.main()
