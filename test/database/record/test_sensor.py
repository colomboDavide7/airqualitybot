######################################################
#
# Author: Davide Colombo
# Date: 16/11/21 14:30
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.database.util.record.record as rec
import airquality.database.util.record.time as t
import airquality.database.util.datatype.timestamp as ts
import airquality.adapter.config as c


class TestSensorRecord(unittest.TestCase):

    def setUp(self) -> None:
        self.sensor_rec = rec.SensorRecord()
        self.api_param_rec = rec.APIParamRecord()
        self.time_rec = t.TimeRecord()
        self.sensor_info_rec = rec.SensorInfoRecord(time_rec=self.time_rec)

    ################################ SENSOR RECORD ################################
    def test_successfully_build_sensor_record(self):
        test_data = {c.SENS_NAME: 'n1', c.SENS_TYPE: 't1'}
        actual_output = self.sensor_rec.record(test_data)
        expected_output = "('t1', 'n1')"
        self.assertEqual(actual_output, expected_output)

    def test_exit_on_missing_sensor_name(self):
        test_data = {c.SENS_TYPE: 't1'}
        with self.assertRaises(SystemExit):
            self.sensor_rec.record(test_data)

    def test_exit_on_missing_sensor_type(self):
        test_data = {c.SENS_NAME: 'n1'}
        with self.assertRaises(SystemExit):
            self.sensor_rec.record(test_data)

    ################################ API PARAM RECORD ################################
    def test_successfully_build_api_param_record(self):
        test_data = {c.SENS_PARAM: [{c.PAR_NAME: 'n1', c.PAR_VAL: 33}, {c.PAR_NAME: 'n2', c.PAR_VAL: 0.2}]}
        actual_output = self.api_param_rec.record(test_data, sensor_id=144)
        expected_output = "(144, 'n1', '33'),(144, 'n2', '0.2')"
        self.assertEqual(actual_output, expected_output)

    def test_exit_on_empty_param(self):
        test_data = {c.SENS_PARAM: []}
        with self.assertRaises(SystemExit):
            self.api_param_rec.record(test_data, sensor_id=144)

    def test_exit_on_missing_param(self):
        test_data = {'other': 1}
        with self.assertRaises(SystemExit):
            self.api_param_rec.record(test_data, sensor_id=144)

    def test_exit_on_missing_param_name_or_value_items(self):
        test_data = {c.SENS_PARAM: [{'other': 'n1', c.PAR_VAL: 33}, {c.PAR_NAME: 'n2', 'other': 0.2}]}
        with self.assertRaises(SystemExit):
            self.api_param_rec.record(test_data, sensor_id=144)

    def test_exit_on_missing_sensor_id_api_param_record(self):
        test_data = {'param_name': ['n1'], 'param_value': [33]}
        with self.assertRaises(SystemExit):
            self.api_param_rec.record(test_data)

    ################################ SENSOR INFO RECORD ################################
    def test_successfully_build_sensor_info_record(self):
        test_data = {c.SENS_INFO: [{c.SENS_CH: 'ch1',
                                    c.TIMEST: {c.CLS: ts.UnixTimestamp, c.KW: {'timestamp': 1531432748}}}
                                   ]}
        actual_output = self.sensor_info_rec.record(test_data, sensor_id=99)
        expected_output = "(99, 'ch1', '2018-07-12 23:59:08')"
        self.assertEqual(actual_output, expected_output)

    def test_exit_on_empty_info(self):
        test_data = {c.SENS_INFO: []}
        with self.assertRaises(SystemExit):
            self.sensor_info_rec.record(test_data, sensor_id=99)

    def test_exit_on_missing_info(self):
        test_data = {'other': 'val'}
        with self.assertRaises(SystemExit):
            self.sensor_info_rec.record(test_data, sensor_id=99)

    def test_exit_on_missing_info_key_items(self):
        test_missing_channel = {c.SENS_INFO: [{'other': 'ch1',
                                               c.TIMEST: {c.CLS: ts.UnixTimestamp, c.KW: {'timestamp': 1531432748}}}
                                              ]}
        with self.assertRaises(SystemExit):
            self.sensor_info_rec.record(test_missing_channel, sensor_id=99)

        test_missing_channel = {c.SENS_INFO: [{c.SENS_CH: 'ch1',
                                          'other': {c.CLS: ts.UnixTimestamp, c.KW: {'timestamp': 1531432748}}}
                                              ]}
        with self.assertRaises(SystemExit):
            self.sensor_info_rec.record(test_missing_channel, sensor_id=99)

    def test_exit_on_missing_sensor_id_sensor_info_record(self):
        test_data = {'channel': ['ch1'], 'last_acquisition': [{'timestamp': 1531432748}]}
        with self.assertRaises(SystemExit):
            self.sensor_info_rec.record(test_data)


if __name__ == '__main__':
    unittest.main()
