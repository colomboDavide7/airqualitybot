######################################################
#
# Author: Davide Colombo
# Date: 16/11/21 14:30
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.database.util.record.record as rec
import airquality.database.util.record.location as loc
import airquality.database.util.postgis.geom as geom
import airquality.database.util.record.time as t
import airquality.database.util.datatype.timestamp as ts


class TestSensorRecord(unittest.TestCase):

    def setUp(self) -> None:
        self.sensor_rec = rec.SensorRecord()
        self.api_param_rec = rec.APIParamRecord()
        self.point_builder = geom.PointBuilder()
        self.location_rec = loc.LocationRecord(self.point_builder)
        self.purpleair_ts_class = ts.UnixTimestamp
        self.time_rec = t.TimeRecord(timestamp_class=self.purpleair_ts_class)
        self.sensor_location_rec = rec.SensorLocationRecord(location_rec=self.location_rec, time_rec=self.time_rec)
        self.sensor_info_rec = rec.SensorInfoRecord(time_rec=self.time_rec)

    ################################ SENSOR RECORD ################################
    def test_successfully_build_sensor_record(self):
        test_data = {'name': 'n1', 'type': 't1'}
        actual_output = self.sensor_rec.record(test_data)
        expected_output = "('t1', 'n1')"
        self.assertEqual(actual_output, expected_output)

    def test_exit_on_missing_sensor_name(self):
        test_data = {'type': 't1'}
        with self.assertRaises(SystemExit):
            self.sensor_rec.record(test_data)

    def test_exit_on_missing_sensor_type(self):
        test_data = {'name': 'n1'}
        with self.assertRaises(SystemExit):
            self.sensor_rec.record(test_data)

    ################################ API PARAM RECORD ################################
    def test_successfully_build_api_param_record(self):
        test_data = {'param_name': ['n1', 'n2'], 'param_value': [33, 0.2]}
        actual_output = self.api_param_rec.record(test_data, sensor_id=144)
        expected_output = "(144, 'n1', '33'),(144, 'n2', '0.2')"
        self.assertEqual(actual_output, expected_output)

    def test_exit_on_missing_param_names(self):
        test_data = {'param_value': [33, 0.2]}
        with self.assertRaises(SystemExit):
            self.api_param_rec.record(test_data, sensor_id=144)

    def test_exit_on_missing_param_values(self):
        test_data = {'param_name': ['n1', 'n2']}
        with self.assertRaises(SystemExit):
            self.api_param_rec.record(test_data, sensor_id=144)

    def test_exit_on_empty_param_names(self):
        test_data = {'param_name': [], 'param_value': [33, 0.2]}
        with self.assertRaises(SystemExit):
            self.api_param_rec.record(test_data, sensor_id=144)

    def test_exit_on_empty_param_values(self):
        test_data = {'param_name': ['n1', 'n2'], 'param_value': []}
        with self.assertRaises(SystemExit):
            self.api_param_rec.record(test_data, sensor_id=144)

    def test_exit_on_different_param_name_values_length(self):
        test_data = {'param_name': ['n1'], 'param_value': [33, 0.2]}
        with self.assertRaises(SystemExit):
            self.api_param_rec.record(test_data, sensor_id=144)

    def test_exit_on_missing_sensor_id_api_param_record(self):
        test_data = {'param_name': ['n1'], 'param_value': [33]}
        with self.assertRaises(SystemExit):
            self.api_param_rec.record(test_data)

    ################################ SENSOR INFO RECORD ################################
    def test_successfully_build_sensor_info_record(self):
        test_data = {'channel': ['ch1'], 'last_acquisition': [{'timestamp': 1531432748}]}
        actual_output = self.sensor_info_rec.record(test_data, sensor_id=99)
        expected_output = "(99, 'ch1', '2018-07-12 23:59:08')"
        self.assertEqual(actual_output, expected_output)

    def test_exit_on_missing_channel_names(self):
        test_data = {'last_acquisition': [{'timestamp': 1531432748}]}
        with self.assertRaises(SystemExit):
            self.sensor_info_rec.record(test_data, sensor_id=99)

    def test_exit_on_empty_channel_name(self):
        test_data = {'channel': [], 'last_acquisition': [{'timestamp': 1531432748}]}
        with self.assertRaises(SystemExit):
            self.sensor_info_rec.record(test_data, sensor_id=99)

    def test_exit_on_missing_acquisitions(self):
        test_data = {'channel': ['ch1']}
        with self.assertRaises(SystemExit):
            self.sensor_info_rec.record(test_data, sensor_id=99)

    def test_exit_on_empty_acquisitions(self):
        test_data = {'channel': ['ch1'], 'last_acquisition': []}
        with self.assertRaises(SystemExit):
            self.sensor_info_rec.record(test_data, sensor_id=99)

    def test_exit_on_different_channel_acquisition_length(self):
        test_data = {'channel': ['ch1', 'ch2'], 'last_acquisition': [{'timestamp': 1531432748}]}
        with self.assertRaises(SystemExit):
            self.sensor_info_rec.record(test_data, sensor_id=99)

    def test_exit_on_missing_sensor_id_sensor_info_record(self):
        test_data = {'channel': ['ch1'], 'last_acquisition': [{'timestamp': 1531432748}]}
        with self.assertRaises(SystemExit):
            self.sensor_info_rec.record(test_data)


if __name__ == '__main__':
    unittest.main()
