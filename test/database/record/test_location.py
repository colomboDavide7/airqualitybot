######################################################
#
# Author: Davide Colombo
# Date: 16/11/21 12:28
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.database.util.record.record as rec
import airquality.database.util.postgis.geom as geom
import airquality.database.util.datatype.timestamp as ts


# class TestLocationRecord(unittest.TestCase):
#
#     def setUp(self) -> None:
#         self.sensor_location_record = rec.SensorLocationRecord()
#
#     def test_successfully_build_sensor_location_record(self):
#         test_data = {'geom': {'class': geom.PointBuilder, 'kwargs': {'lat': '45.123', 'lng': 9.123}},
#                      'timestamp': {'class': ts.SQLTimestamp, 'kwargs': {'timestamp': '2018-07-12 11:44:00'}}}
#         expected_output = "(1, '2018-07-12 11:44:00', ST_GeomFromText('POINT(9.123 45.123)', 26918))"
#         actual_output = self.sensor_location_record.record(sensor_data=test_data, sensor_id=1)
#         self.assertEqual(actual_output, expected_output)
#
#     def test_exit_on_missing_geom(self):
#         test_data = {'opt': 'val', 'timestamp': {'class': ts.CurrentTimestamp, 'kwargs': {}}}
#         with self.assertRaises(SystemExit):
#             self.sensor_location_record.record(sensor_data=test_data, sensor_id=1)
#
#     def test_exit_on_empty_geom(self):
#         test_data = {'geom': {}, 'timestamp': {'class': ts.CurrentTimestamp, 'kwargs': {}}}
#         with self.assertRaises(SystemExit):
#             self.sensor_location_record.record(sensor_data=test_data, sensor_id=1)
#
#     def test_exit_on_missing_class_or_kwargs_inside_geom(self):
#         test_data = {'geom': {'class': geom.PointBuilder, 'other': 2},
#                      'timestamp': {'class': ts.CurrentTimestamp, 'kwargs': {}}}
#         with self.assertRaises(SystemExit):
#             self.sensor_location_record.record(sensor_data=test_data, sensor_id=1)
#
#     def test_null_value_when_null_object_is_passed(self):
#         test_data = {'geom': {'class': geom.NullGeometry, 'kwargs': {}},
#                      'timestamp': {'class': ts.SQLTimestamp, 'kwargs': {'timestamp': '2018-07-12 11:44:00'}}}
#         expected_output = "(1, '2018-07-12 11:44:00', NULL)"
#         actual_output = self.sensor_location_record.record(sensor_data=test_data, sensor_id=1)
#         self.assertEqual(actual_output, expected_output)
#
#
# if __name__ == '__main__':
#     unittest.main()
