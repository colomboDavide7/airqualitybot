######################################################
#
# Author: Davide Colombo
# Date: 16/11/21 12:28
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.database.util.record.location as loc
import airquality.database.util.postgis.geom as geom
import airquality.adapter.config as c


class TestLocationRecord(unittest.TestCase):

    def setUp(self) -> None:
        self.location_rec = loc.LocationRecord()

    def test_successfully_build_sensor_location_record(self):
        test_data = {c.SENS_GEOM: {c.CLS: geom.PointBuilder, c.KW: {'lat': '45.123', 'lng': 9.123}}}
        expected_output = "ST_GeomFromText('POINT(9.123 45.123)', 26918)"
        actual_output = self.location_rec.record(sensor_data=test_data)
        self.assertEqual(actual_output, expected_output)

    def test_exit_on_missing_geom(self):
        test_data = {'opt': 'val'}
        with self.assertRaises(SystemExit):
            self.location_rec.record(sensor_data=test_data)

    def test_exit_on_empty_geom(self):
        test_data = {c.SENS_GEOM: {}}
        with self.assertRaises(SystemExit):
            self.location_rec.record(sensor_data=test_data)

    def test_exit_on_missing_class_or_kwargs_inside_geom(self):
        test_data = {c.SENS_GEOM: {c.CLS: geom.PointBuilder, 'other': 2}}
        with self.assertRaises(SystemExit):
            self.location_rec.record(sensor_data=test_data)

    def test_null_value_when_null_object_is_passed(self):
        test_data = {c.SENS_GEOM: {c.CLS: geom.NullGeometry, c.KW: {}}}
        expected_output = "NULL"
        actual_output = self.location_rec.record(sensor_data=test_data)
        self.assertEqual(actual_output, expected_output)


if __name__ == '__main__':
    unittest.main()
