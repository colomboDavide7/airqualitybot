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


class TestMeasurementRecord(unittest.TestCase):

    def setUp(self) -> None:
        self.atmotube_time_rec = t.TimeRecord(timestamp_class=ts.AtmotubeTimestamp)
        self.mobile_rec = rec.MobileMeasureRecord(time_rec=self.atmotube_time_rec)

        self.thingspeak_time_rec = t.TimeRecord(timestamp_class=ts.ThingspeakTimestamp)
        self.station_rec = rec.StationMeasureRecord(self.thingspeak_time_rec)

    ################################ STATION MEASUREMENT RECORD ################################
    def test_successfully_build_station_record(self):
        test_data = {'record_id': 99, 'param': [{'id': 1, 'val': 55}], 'timestamp': '2018-10-11T09:44:00Z'}
        actual_output = self.station_rec.record(test_data, sensor_id=144)
        expected_output = "(99, 1, 144, '55', '2018-10-11 09:44:00')"
        self.assertEqual(actual_output, expected_output)

    def test_exit_when_missing_sensor_id(self):
        test_data = {'record_id': 99, 'param_id': [1], 'param_value': [55], 'timestamp': '2018-10-11T09:44:00Z'}
        with self.assertRaises(SystemExit):
            self.station_rec.record(test_data)

    ################################ MOBILE MEASUREMENT RECORD ################################
    def test_successfully_build_mobile_record(self):
        test_data = {'record_id': 99, 'param': [{'id': 1, 'val': 55}], 'timestamp': '2018-10-11T09:44:00.000Z',
                     'geom': {'class': geom.PointBuilder, 'kwargs': {'lat': '45', 'lng': '9'}}}
        actual_output = self.mobile_rec.record(sensor_data=test_data)
        expected_output = "(99, 1, '55', '2018-10-11 09:44:00', ST_GeomFromText('POINT(9 45)', 26918))"
        self.assertEqual(actual_output, expected_output)

    def test_exit_on_missing_record_id_mobile_record(self):
        test_missing_record_id = {'param': [{'id': 1, 'val': 55}],
                                  'timestamp': '2018-10-11T09:44:00.000Z',
                                  'geom': {'class': geom.PointBuilder, 'kwargs': {'lat': '45', 'lng': '9'}}}
        with self.assertRaises(SystemExit):
            self.mobile_rec.record(test_missing_record_id)

    def test_exit_on_missing_param(self):
        test_missing_param = {'record_id': 99,
                              'timestamp': '2018-10-11T09:44:00.000Z',
                              'geom': {'class': geom.PointBuilder, 'kwargs': {'lat': '45', 'lng': '9'}}}
        with self.assertRaises(SystemExit):
            rec._exit_on_missing_measure_param_data(test_missing_param)

    def test_exit_on_empty_param_list(self):
        test_missing_param_val = {'record_id': 99, 'param': [],
                                  'timestamp': '2018-10-11T09:44:00.000Z',
                                  'geom': {'class': geom.PointBuilder, 'kwargs': {'lat': '45', 'lng': '9'}}}
        with self.assertRaises(SystemExit):
            rec._exit_on_missing_measure_param_data(test_missing_param_val)

    def test_exit_on_missing_param_id_or_param_value(self):
        test_missing_param_id = {'record_id': 99, 'param': [{'val': 55}],
                                 'timestamp': '2018-10-11T09:44:00.000Z',
                                 'geom': {'class': geom.PointBuilder, 'kwargs': {'lat': '45', 'lng': '9'}}}
        with self.assertRaises(SystemExit):
            self.mobile_rec.record(test_missing_param_id)


if __name__ == '__main__':
    unittest.main()
