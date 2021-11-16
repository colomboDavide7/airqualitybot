######################################################
#
# Author: Davide Colombo
# Date: 16/11/21 12:40
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.database.util.record.record as rec
import airquality.database.util.record.time as t
import airquality.database.util.datatype.timestamp as ts
import airquality.database.util.postgis.geom as geom
import airquality.database.util.record.location as loc


class TestMeasurementRecord(unittest.TestCase):

    def setUp(self) -> None:
        self.atmotube_time_rec = t.TimeRecord(timestamp_class=ts.AtmotubeTimestamp)
        self.atmotube_location_rec = loc.LocationRecord(postgis_builder=geom.PointBuilder())
        self.mobile_rec = rec.MobileMeasureRecord(time_rec=self.atmotube_time_rec,
                                                  location_rec=self.atmotube_location_rec)

        self.thingspeak_time_rec = t.TimeRecord(timestamp_class=ts.ThingspeakTimestamp)
        self.station_rec = rec.StationMeasureRecord(self.thingspeak_time_rec)

    def test_successfully_build_station_record(self):
        test_data = {'record_id': 99, 'param_id': [1], 'param_value': [55], 'timestamp': '2018-10-11T09:44:00Z'}
        actual_output = self.station_rec.record(test_data, sensor_id=144)
        expected_output = "(99, 1, 144, '55', '2018-10-11 09:44:00')"
        self.assertEqual(actual_output, expected_output)

    def test_exit_when_missing_sensor_id(self):
        test_data = {'record_id': 99, 'param_id': [1], 'param_value': [55], 'timestamp': '2018-10-11T09:44:00Z'}
        with self.assertRaises(SystemExit):
            self.station_rec.record(test_data)

    def test_successfully_build_mobile_record(self):
        test_data = {'record_id': 99, 'param_id': [1], 'param_value': [55], 'timestamp': '2018-10-11T09:44:00.000Z',
                     'lat': '45', 'lng': '9'}
        actual_output = self.mobile_rec.record(sensor_data=test_data)
        expected_output = "(99, 1, '55', '2018-10-11 09:44:00', ST_GeomFromText('POINT(9 45)', 26918))"
        self.assertEqual(actual_output, expected_output)

    def test_exit_on_missing_record_id_mobile_record(self):
        test_missing_record_id = {'param_id': [1], 'param_value': [55],
                                  'timestamp': '2018-10-11T09:44:00.000Z',
                                  'lat': '45', 'lng': '9'}
        with self.assertRaises(SystemExit):
            self.mobile_rec.record(test_missing_record_id)

    def test_exit_on_missing_param_id_mobile_record(self):
        test_missing_param_id = {'record_id': 99, 'param_value': [55],
                                 'timestamp': '2018-10-11T09:44:00.000Z',
                                 'lat': '45', 'lng': '9'}
        with self.assertRaises(SystemExit):
            self.mobile_rec.record(test_missing_param_id)

    def test_exit_on_missing_param_value_mobile_record(self):
        test_missing_param_val = {'record_id': 99, 'param_id': [1],
                                  'timestamp': '2018-10-11T09:44:00.000Z',
                                  'lat': '45', 'lng': '9'}
        with self.assertRaises(SystemExit):
            self.mobile_rec.record(test_missing_param_val)

    def test_exit_on_different_id_value_length(self):
        test_different_id_value_length = {'record_id': 99, 'param_id': [1, 2], 'param_value': [55],
                                          'timestamp': '2018-10-11T09:44:00.000Z',
                                          'lat': '45', 'lng': '9'}
        with self.assertRaises(SystemExit):
            self.mobile_rec.record(test_different_id_value_length)

    def test_exit_on_empty_id_value_lists(self):
        test_empty_id_value = {'record_id': 99, 'param_id': [], 'param_value': [],
                               'timestamp': '2018-10-11T09:44:00.000Z',
                               'lat': '45', 'lng': '9'}
        with self.assertRaises(SystemExit):
            self.mobile_rec.record(test_empty_id_value)


if __name__ == '__main__':
    unittest.main()
