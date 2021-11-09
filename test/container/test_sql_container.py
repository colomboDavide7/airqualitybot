######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 09/11/21 12:35
# Description: INSERT HERE THE DESCRIPTION
#
######################################################

import unittest
from airquality.container.sql_container import SensorSQLContainer, APIParamSQLContainer, GeoSQLContainer


class TestSQLContainer(unittest.TestCase):

    def test_sql_from_sensor_container(self):
        sensor_container = SensorSQLContainer(sensor_name='test name', sensor_type='test type')
        actual_output = sensor_container.sql(query='query statement ')
        expected_output = "query statement ('test type', 'test name')"
        self.assertEqual(actual_output, expected_output)

    def test_sql_from_api_container(self):
        test_names = ['n1', 'n2']
        test_values = ['v1', 'v2']
        api_container = APIParamSQLContainer(sensor_id=1, param_name=test_names, param_value=test_values)
        actual_output = api_container.sql(query='query statement ')
        expected_output = "query statement (1, 'n1', 'v1'),(1, 'n2', 'v2')"
        self.assertEqual(actual_output, expected_output)

    def test_sql_geo_container(self):
        geo_container = GeoSQLContainer(sensor_id=1, valid_from='ts', geom='g')
        actual_output = geo_container.sql(query='query statement ')
        expected_output = "query statement (1, 'ts', g)"
        self.assertEqual(actual_output, expected_output)


if __name__ == '__main__':
    unittest.main()
