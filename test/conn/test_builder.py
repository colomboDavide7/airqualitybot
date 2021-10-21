#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 10:32
# @Description: This script defines the test for the SQLQueryBuilder class
#
#################################################

import unittest
from airquality.conn.builder import SQLQueryBuilder


class TestSQLQueryBuilder(unittest.TestCase):
    """Class for testing the sql query builder."""

    def setUp(self) -> None:
        self.model = "Atmotube Pro"

    def test_system_exit_with_empty_models(self):
        """Test SystemExit when mobile model list is passed."""

        models = []
        with self.assertRaises(SystemExit):
            SQLQueryBuilder.select_mobile_sensor_ids(models)




if __name__ == '__main__':
    unittest.main()
