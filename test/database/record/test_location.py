######################################################
#
# Author: Davide Colombo
# Date: 16/11/21 12:28
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import database.record.georec as loc
import database.postgis.geom as geom
import airquality.adapter.config as adapt_const
import database.postgis.config as geom_const


class TestLocationRecord(unittest.TestCase):

    def setUp(self) -> None:
        self.location_rec = loc.LocationRecord()

    def test_successfully_build_sensor_location_record(self):
        test_data = {adapt_const.SENS_GEOM: {adapt_const.CLS: geom.PostgisPoint,
                                             adapt_const.KW: {geom_const.POINT_INIT_LAT_NAME: '45.123',
                                                              geom_const.POINT_INIT_LNG_NAME: 9.123}}}
        expected_output = "ST_GeomFromText('POINT(9.123 45.123)', 26918)"
        actual_output = self.location_rec.record(sensor_data=test_data)
        self.assertEqual(actual_output, expected_output)

    def test_exit_on_missing_geom(self):
        test_data = {'opt': 'val'}
        with self.assertRaises(SystemExit):
            self.location_rec.record(sensor_data=test_data)

    def test_exit_on_empty_geom(self):
        test_data = {adapt_const.SENS_GEOM: {}}
        with self.assertRaises(SystemExit):
            self.location_rec.record(sensor_data=test_data)

    def test_exit_on_missing_class_or_kwargs_inside_geom(self):
        test_data = {adapt_const.SENS_GEOM: {adapt_const.CLS: geom.PostgisPoint, 'other': 2}}
        with self.assertRaises(SystemExit):
            self.location_rec.record(sensor_data=test_data)

    def test_null_value_when_null_object_is_passed(self):
        test_data = {adapt_const.SENS_GEOM: {adapt_const.CLS: geom.NullGeometry, adapt_const.KW: {}}}
        expected_output = "NULL"
        actual_output = self.location_rec.record(sensor_data=test_data)
        self.assertEqual(actual_output, expected_output)


if __name__ == '__main__':
    unittest.main()
