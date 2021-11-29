######################################################
#
# Author: Davide Colombo
# Date: 29/11/21 20:20
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.database.rec.measure as rec
import airquality.types.postgis as pgis
import airquality.types.timestamp as ts


class TestMeasureRecord(unittest.TestCase):

    def setUp(self) -> None:
        self.mobile_record_builder = rec.MobileRecordBuilder()
        self.station_record_builder = rec.StationRecordBuilder()
        self.name2id = {'p1': 1, 'p2': 2, 'p3': 3}

    def test_successfully_get_mobile_measure(self):
        self.mobile_record_builder.with_measure_name2id(self.name2id)
        self.mobile_record_builder.with_sensor_id(99)
        self.mobile_record_builder.with_geometry(pgis.PostgisPoint(lat="l1", lng="l2"))
        actual = self.mobile_record_builder.get_measure_value(
            record_id=12, timestamp=ts.SQLTimestamp("2021-10-11 09:44:00"), param_name="p1", param_value="88"
        )
        expected = "(12, 1, '88', '2021-10-11 09:44:00', ST_GeomFromText('POINT(l2 l1)', 26918))"
        self.assertEqual(actual, expected)

    def test_successfully_get_mobile_measure_when_value_is_none(self):
        self.mobile_record_builder.with_measure_name2id(self.name2id)
        self.mobile_record_builder.with_sensor_id(99)
        self.mobile_record_builder.with_geometry(pgis.NullGeometry())
        actual = self.mobile_record_builder.get_measure_value(
            record_id=12, timestamp=ts.SQLTimestamp("2021-10-11 09:44:00"), param_name="p1", param_value=None
        )
        expected = "(12, 1, NULL, '2021-10-11 09:44:00', NULL)"
        self.assertEqual(actual, expected)

    def test_successfully_get_station_measure_value(self):
        self.station_record_builder.with_measure_name2id(self.name2id)
        self.station_record_builder.with_sensor_id(99)
        actual = self.station_record_builder.get_measure_value(
            record_id=44, timestamp=ts.SQLTimestamp("2021-10-11 09:44:00"), param_name="p2", param_value="33"
        )
        expected = "(44, 2, 99, '33', '2021-10-11 09:44:00')"
        self.assertEqual(actual, expected)

    def test_successfully_get_station_measure_value_when_param_value_is_none(self):
        self.station_record_builder.with_measure_name2id(self.name2id)
        self.station_record_builder.with_sensor_id(99)
        actual = self.station_record_builder.get_measure_value(
            record_id=44, timestamp=ts.SQLTimestamp("2021-10-11 09:44:00"), param_name="p2", param_value=None
        )
        expected = "(44, 2, 99, NULL, '2021-10-11 09:44:00')"
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
