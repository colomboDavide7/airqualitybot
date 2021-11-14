######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 09/11/21 12:35
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.database.util.sql.record as rec


class TestSQLBuilder(unittest.TestCase):

    def test_sensor_record(self):
        test_packet = {'name': 'n1', 'type': 't1'}
        record = rec.SensorRecord(sensor_id=1, packet=test_packet)
        actual_output = record.record()
        expected_output = "('t1', 'n1')"
        self.assertEqual(actual_output, expected_output)

    def test_system_exit_when_key_error_is_raised_sensor(self):
        test_missing_type = {'name': 'n1', }
        with self.assertRaises(SystemExit):
            rec.SensorRecord(sensor_id=1, packet=test_missing_type)

        test_missing_name = {'type': 't1'}
        with self.assertRaises(SystemExit):
            rec.SensorRecord(sensor_id=1, packet=test_missing_name)

    def test_api_param_record(self):
        test_packet = {'param_name': ['n1', 'n2'], 'param_value': ['v1', 'v2']}
        record = rec.APIParamRecord(sensor_id=1, packet=test_packet)
        actual_output = record.record()
        expected_output = "(1, 'n1', 'v1'),(1, 'n2', 'v2')"
        self.assertEqual(actual_output, expected_output)

    def test_system_exit_when_key_error_is_raised_api_param_record(self):
        test_missing_value = {'param_name': ['n1', 'n2']}
        with self.assertRaises(SystemExit):
            rec.APIParamRecord(sensor_id=1, packet=test_missing_value)

        test_missing_name = {'param_value': ['v1', 'v2']}
        with self.assertRaises(SystemExit):
            rec.APIParamRecord(sensor_id=1, packet=test_missing_name)

        test_empty_list = {'param_name': [], 'param_value': []}
        with self.assertRaises(SystemExit):
            rec.APIParamRecord(sensor_id=1, packet=test_empty_list)

        test_different_length = {'param_name': ['n1'], 'param_value': []}
        with self.assertRaises(SystemExit):
            rec.APIParamRecord(sensor_id=1, packet=test_different_length)

        test_different_length = {'param_name': ['n1'], 'param_value': ['v1', 'v2']}
        with self.assertRaises(SystemExit):
            rec.APIParamRecord(sensor_id=1, packet=test_different_length)

    def test_location_record(self):
        geo_container = rec.LocationRecord(sensor_id=1, valid_from='ts', geom='g')
        actual_output = geo_container.record()
        expected_output = "(1, 'ts', g)"
        self.assertEqual(actual_output, expected_output)

    def test_sensor_info_record(self):
        test_packet = {'channel': ['ch1', 'ch2'], 'last_acquisition': ['ts1', 'ts2']}
        record = rec.SensorInfoRecord(sensor_id=1, packet=test_packet)
        actual_output = record.record()
        expected_output = "(1, 'ch1', 'ts1'),(1, 'ch2', 'ts2')"
        self.assertEqual(actual_output, expected_output)

    def test_system_exit_when_key_error_is_raised_sensor_info_record(self):
        test_missing_channel = {'last_acquisition': ['ts1', 'ts2']}
        with self.assertRaises(SystemExit):
            rec.SensorInfoRecord(sensor_id=1, packet=test_missing_channel)

        test_missing_last_acq = {'channel': 'ch1'}
        with self.assertRaises(SystemExit):
            rec.SensorInfoRecord(sensor_id=1, packet=test_missing_last_acq)

        test_different_length = {'channel': ['ch1'], 'last_acquisition': []}
        with self.assertRaises(SystemExit):
            rec.SensorInfoRecord(sensor_id=1, packet=test_different_length)

        test_different_length = {'channel': ['ch1'], 'last_acquisition': ['ts1', 'ts2']}
        with self.assertRaises(SystemExit):
            rec.SensorInfoRecord(sensor_id=1, packet=test_different_length)

        test_empty_channel = {'channel': [], 'last_acquisition': []}
        with self.assertRaises(SystemExit):
            rec.SensorInfoRecord(sensor_id=1, packet=test_empty_channel)




if __name__ == '__main__':
    unittest.main()
