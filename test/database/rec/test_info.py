######################################################
#
# Author: Davide Colombo
# Date: 29/11/21 14:55
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.database.rec.info as rec
import airquality.types.timestamp as ts
import airquality.types.postgis as pgis


class TestSensorInfoRecord(unittest.TestCase):

    def setUp(self) -> None:
        self.record_builder = rec.InfoRecordBuilder()

    def test_successfully_get_sensor_value(self):
        self.record_builder.with_sensor_id(sensor_id=1)
        actual = self.record_builder.get_sensor_value(sensor_name="n1", sensor_type="t1")
        expected = "(1, 't1', 'n1'),"
        self.assertEqual(actual, expected)

    def test_successfully_get_api_param_value(self):
        self.record_builder.with_sensor_id(99)
        actual = self.record_builder.get_api_param_values(
            ident="id", key="k", name="n", timest=ts.SQLTimestamp(timest="2021-10-11 00:39:00")
        )
        expected = "(99, 'k', 'id', 'n', '2021-10-11 00:39:00')"
        self.assertEqual(actual, expected)

    def test_successfully_get_geolocation_value(self):
        self.record_builder.with_sensor_id(1000)
        actual = self.record_builder.get_geolocation_value(
            timest=ts.SQLTimestamp("2021-10-11 00:39:00"), geometry=pgis.NullGeometry()
        )
        expected = "(1000, '2021-10-11 00:39:00', NULL),"
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
