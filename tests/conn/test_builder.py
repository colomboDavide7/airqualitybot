#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 10:32
# @Description: This script defines the tests for the SQLQueryBuilder class
#
#################################################

import unittest
from airquality.conn.builder import SQLQueryBuilder


class TestSQLQueryBuilder(unittest.TestCase):


    def setUp(self) -> None:
        self.model = "Atmotube Pro"

    def test_system_exit_select_atmotube_ids(self):
        """Test SystemExit exception when bad model name is passed."""

        with self.assertRaises(SystemExit):
            SQLQueryBuilder.select_all_sensor_ids_by_model("bad_model_name")




if __name__ == '__main__':
    unittest.main()
