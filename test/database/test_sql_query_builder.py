#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 10:32
# @Description: unit test script
#
#################################################
import unittest
from airquality.constants.shared_constants import EMPTY_STRING, EMPTY_LIST
from airquality.database.sql_query_builder import SQLQueryBuilder


class TestSQLQueryBuilder(unittest.TestCase):


    def setUp(self) -> None:
        """This method is run every time before a test is run."""
        self.sql_builder = SQLQueryBuilder(query_file_path = "properties/sql_query.json")


    def test_system_exit_when_query_identifier_not_found(self):
        test_query_id = "bad query identifier"
        with self.assertRaises(SystemExit):
            self.sql_builder._raise_exception_if_query_identifier_not_found(query_id = test_query_id)


    def test_empty_query_when_empty_packet_list_insert_atmotube_measurement(self):
        """This method test the return value of 'EMPTY_STRING' when an EMPTY_LIST is passed as argument."""

        test_packets = EMPTY_LIST
        expected_output = EMPTY_STRING
        actual_output = self.sql_builder.insert_atmotube_measurement_packets(packets = test_packets)
        self.assertEqual(actual_output, expected_output)


    def test_empty_query_when_empty_timestamp_update_last_date_atmotube(self):
        """This method test the return value of 'EMPTY_STRING' when an EMPTY_STRING is passed as argument."""

        test_timestamp = EMPTY_STRING
        expected_output = EMPTY_STRING
        actual_output = self.sql_builder.update_last_packet_date_atmotube(last_timestamp = test_timestamp,
                                                                          sensor_id = 1)
        self.assertEqual(actual_output, expected_output)


    def test_empty_query_if_empty_packet_list_when_insert_sensor(self):
        """This method test the return value of 'EMPTY_STRING' when an EMPTY_LIST is passed as argument."""

        expected_output = EMPTY_STRING
        actual_output = self.sql_builder.insert_sensors_from_identifier(packets = EMPTY_LIST, identifier = "purpleair")
        self.assertEqual(actual_output, expected_output)



if __name__ == '__main__':
    unittest.main()
