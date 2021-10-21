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
        self.sql_builder = SQLQueryBuilder(query_file_path = "properties/sql_query.json")

    def test_select_mobile_sensor_ids(self):

        query = self.sql_builder.select_mobile_sensor_ids(["model1", "model2"])
        self.assertIsNotNone(query)
        self.assertIsInstance(query, str)


    def test_system_exit_with_empty_models(self):
        """Test SystemExit when mobile model list is passed."""

        models = []
        with self.assertRaises(SystemExit):
            self.sql_builder.select_mobile_sensor_ids(models)




if __name__ == '__main__':
    unittest.main()
