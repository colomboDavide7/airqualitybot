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


class TestLocationRecord(unittest.TestCase):

    def setUp(self) -> None:
        self.point_builder = geom.PointBuilder()
        self.location_rec = loc.LocationRecord(self.point_builder)

    def test_point_geometry_record(self):
        test_data = {'lat': 'l1', 'lng': 'l2'}
        actual_output = self.location_rec.record(test_data)
        expected_output = "ST_GeomFromText('POINT(l2 l1)', 26918)"
        self.assertEqual(actual_output, expected_output)

    def test_point_geometry_record_when_missing_coords(self):
        test_data = {'other': 'v'}
        actual_output = self.location_rec.record(test_data)
        expected_output = "NULL"
        self.assertEqual(actual_output, expected_output)

    def test_exit_on_partial_coords(self):
        test_data = {'lat': 'l1'}
        with self.assertRaises(SystemExit):
            self.location_rec.record(test_data)

        test_data = {'lng': 'l1'}
        with self.assertRaises(SystemExit):
            self.location_rec.record(test_data)


if __name__ == '__main__':
    unittest.main()
