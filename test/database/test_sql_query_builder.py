#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 10:32
# @Description: unit test script
#
#################################################

import unittest
from airquality.database.sql_query_builder import SQLQueryBuilder


class TestSQLQueryBuilder(unittest.TestCase):
    """Class for testing the sql query builder."""

    def setUp(self) -> None:
        self.sql_builder = SQLQueryBuilder(query_file_path = "properties/test_sql_query.json")

    def test_system_exit_select_sensor_ids_bad_query_identifier(self):

        with self.assertRaises(SystemExit):
            self.sql_builder.select_sensor_ids_from_identifier(identifier = "test identifier")

    def test_system_exit_select_api_param_bad_query_identifier(self):

        with self.assertRaises(SystemExit):
            self.sql_builder.select_api_param_from_sensor_id(sensor_id = 1)



if __name__ == '__main__':
    unittest.main()
