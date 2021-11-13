######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 13/11/21 15:56
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import adapter as msr


class TestMeasureReshaper(unittest.TestCase):

    def test_get_measure_reshaper_class(self):
        obj_cls = msr.get_measure_reshaper_class(sensor_type='atmotube')
        self.assertEqual(obj_cls, msr.AtmotubeMeasureReshaper)

        obj_cls = msr.get_measure_reshaper_class(sensor_type='thingspeak')
        self.assertEqual(obj_cls, msr.ThingspeakMeasureReshaper)

        with self.assertRaises(SystemExit):
            msr.get_measure_reshaper_class(sensor_type='bad sensor type')

    ############################## TEST ATMOTUBE MEASURE RESHAPER #############################
    def test_successfully_reshape_atmotube_measurements(self):
        test_packet = {'voc': 'val1', 'pm1': 'val2', 'pm25': 'val3', 'pm10': 'val4', 't': 'val5', 'h': 'val6',
                       'p': 'val7', 'time': '2021-10-11T01:33:44.000Z'}
        expected_output = {'timestamp': '2021-10-11T01:33:44.000Z',
                           'param_name': ['voc', 'pm1', 'pm25', 'pm10', 't', 'h', 'p'],
                           'param_value': ['val1', 'val2', 'val3', 'val4', 'val5', 'val6', 'val7']}
        actual_output = msr.AtmotubeMeasureReshaper(test_packet).reshape()
        self.assertEqual(actual_output, expected_output)

        # Test when 'coords' are not missing
        test_packet = {'voc': 'val1', 'pm1': 'val2', 'pm25': 'val3', 'pm10': 'val4', 't': 'val5', 'h': 'val6',
                       'p': 'val7', 'time': '2021-10-11T01:33:44.000Z', 'coords': {'lat': 'lat_val', 'lon': 'lon_val'}}
        expected_output = {'lat': 'lat_val', 'lng': 'lon_val', 'timestamp': '2021-10-11T01:33:44.000Z',
                           'param_name': ['voc', 'pm1', 'pm25', 'pm10', 't', 'h', 'p'],
                           'param_value': ['val1', 'val2', 'val3', 'val4', 'val5', 'val6', 'val7']}
        actual_output = msr.AtmotubeMeasureReshaper(test_packet).reshape()
        self.assertEqual(actual_output, expected_output)

    def test_none_value_when_field_is_missing(self):
        # Test output when 't', 'h' and 'p' are missing
        test_packet = {'voc': 'val1', 'pm1': 'val2', 'pm25': 'val3', 'pm10': 'val4', 'time': '2021-10-11T01:33:44.000Z'}
        expected_output = {'timestamp': '2021-10-11T01:33:44.000Z',
                           'param_name': ['voc', 'pm1', 'pm25', 'pm10', 't', 'h', 'p'],
                           'param_value': ['val1', 'val2', 'val3', 'val4', None, None, None]}
        actual_output = msr.AtmotubeMeasureReshaper(test_packet).reshape()
        self.assertEqual(actual_output, expected_output)

    def test_system_exit_when_param_is_missing(self):
        # Test when 'coords' are not missing
        test_packet = {'voc': 'val1', 'pm1': 'val2', 'pm25': 'val3', 'pm10': 'val4', 't': 'val5', 'h': 'val6',
                       'p': 'val7', 'coords': {}}
        with self.assertRaises(SystemExit):
            msr.AtmotubeMeasureReshaper(test_packet).reshape()

    ############################## TEST THINGSPEAK MEASURE RESHAPER #############################
    def test_successfully_adapt_thingspeak_packets(self):
        test_packet = {'created_at': '2021-10-11T01:33:44Z',
                       'fields': [{'name': 'f1', 'value': 'val1'},
                                  {'name': 'f2', 'value': 'val2'}]}

        expected_output = {'timestamp': '2021-10-11T01:33:44Z',
                           'param_name': ['f1', 'f2'],
                           'param_value': ['val1', 'val2']}
        actual_output = msr.ThingspeakMeasureReshaper(test_packet).reshape()
        self.assertEqual(actual_output, expected_output)

    def test_none_value_when_param_is_null(self):
        test_packet = {'created_at': '2021-10-11T01:33:44Z',
                       'fields': [{'name': 'f1', 'value': None},
                                  {'name': 'f2', 'value': 'val2'}]}

        expected_output = {'timestamp': '2021-10-11T01:33:44Z',
                           'param_name': ['f1', 'f2'],
                           'param_value': [None, 'val2']}
        actual_output = msr.ThingspeakMeasureReshaper(test_packet).reshape()
        self.assertEqual(actual_output, expected_output)

    def test_system_exit_when_key_error_is_raised(self):
        test_packet = {'created_at': '2021-10-11T01:33:44Z',
                       'fields': [{'name': 'f1', 'bad_key': 'val1'},
                                  {'name': 'f2', 'bad_key': 'val2'}]}
        with self.assertRaises(SystemExit):
            msr.ThingspeakMeasureReshaper(test_packet).reshape()

        test_packet = {'created_at': '2021-10-11T01:33:44Z',
                       'fields': [{'bad_key': 'f1', 'value': 'val1'},
                                  {'bad_key': 'f2', 'value': 'val2'}]}
        with self.assertRaises(SystemExit):
            msr.ThingspeakMeasureReshaper(test_packet).reshape()

        test_packet = {'created_at': '2021-10-11T01:33:44Z'}
        with self.assertRaises(SystemExit):
            msr.ThingspeakMeasureReshaper(test_packet).reshape()


if __name__ == '__main__':
    unittest.main()
