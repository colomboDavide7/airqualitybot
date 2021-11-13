######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 09/11/21 12:35
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.database.util.sql as sql


class TestSQLBuilder(unittest.TestCase):

    def test_sql_from_sensor_values(self):
        test_packet = {'name': 'n1', 'type': 't1'}
        sensor_values = sql.SensorSQLValueBuilder(sensor_id=1, packet=test_packet)
        actual_output = sensor_values.values()
        expected_output = "('t1', 'n1')"
        self.assertEqual(actual_output, expected_output)

    def test_system_exit_when_key_error_is_raised_sensor_builder(self):
        test_missing_type = {'name': 'n1', }
        with self.assertRaises(SystemExit):
            sql.SensorSQLValueBuilder(sensor_id=1, packet=test_missing_type)

        test_missing_name = {'type': 't1'}
        with self.assertRaises(SystemExit):
            sql.SensorSQLValueBuilder(sensor_id=1, packet=test_missing_name)

    def test_sql_from_api_values(self):
        test_packet = {'param_name': ['n1', 'n2'], 'param_value': ['v1', 'v2']}
        api_container = sql.APIParamSQLValueBuilder(sensor_id=1, packet=test_packet)
        actual_output = api_container.values()
        expected_output = "(1, 'n1', 'v1'),(1, 'n2', 'v2')"
        self.assertEqual(actual_output, expected_output)

    def test_system_exit_when_key_error_is_raise_api_param_builder(self):
        test_missing_value = {'param_name': ['n1', 'n2']}
        with self.assertRaises(SystemExit):
            sql.APIParamSQLValueBuilder(sensor_id=1, packet=test_missing_value)

        test_missing_name = {'param_value': ['v1', 'v2']}
        with self.assertRaises(SystemExit):
            sql.APIParamSQLValueBuilder(sensor_id=1, packet=test_missing_name)

    def test_sql_sensor_at_location_values(self):
        geo_container = sql.LocationSQLValueBuilder(sensor_id=1, valid_from='ts', geom='g')
        actual_output = geo_container.values()
        expected_output = "(1, 'ts', g)"
        self.assertEqual(actual_output, expected_output)


if __name__ == '__main__':
    unittest.main()
