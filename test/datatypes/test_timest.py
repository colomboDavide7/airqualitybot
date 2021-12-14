#################################################
#
# @Author: davidecolombo
# @Date: ven, 22-10-2021, 12:07
# @Description: unit test script
#
#################################################
import unittest
import airquality.types.timest as tstype
import datetime as dt


class TestTimest(unittest.TestCase):

    def setUp(self) -> None:
        self.atmotube_ts1 = tstype.SQLTimest("2021-10-11T09:44:00.000Z", fmt=tstype.ATMOTUBE_FMT)
        self.atmotube_ts2 = tstype.SQLTimest("2018-01-01T00:00:00.000Z", fmt=tstype.ATMOTUBE_FMT)
        self.thingspk_ts1 = tstype.SQLTimest("2021-09-04T17:35:44Z", fmt=tstype.THINGSPK_FMT)
        self.thingspk_ts2 = tstype.SQLTimest("2020-07-14T14:05:09Z", fmt=tstype.THINGSPK_FMT)
        self.current_ts = tstype.CurrentSQLTimest()
        self.unix_ts = tstype.UnixSQLTimest(timest=1531432748)

    def test_add_days_to_atmotube_timestamp(self):
        new_timest = self.atmotube_ts1.add_days(days=1)
        actual_output = new_timest.ts
        expected_output = "2021-10-12 09:44:00"
        self.assertEqual(actual_output, expected_output)

    def test_is_after_atmotube_timestamp(self):
        self.assertFalse(self.atmotube_ts2.is_after(self.atmotube_ts1))
        self.assertTrue(self.atmotube_ts1.is_after(self.atmotube_ts2))

    def test_is_same_day_atmotube_timestamp(self):
        self.assertTrue(self.atmotube_ts1.is_same_day(self.atmotube_ts1))
        self.assertFalse(self.atmotube_ts1.is_same_day(self.atmotube_ts2))

    def test_add_days_to_thingspeak_timestamp(self):
        new_timest = self.thingspk_ts1.add_days(days=10)
        actual_output = new_timest.ts
        expected_output = "2021-09-14 17:35:44"
        self.assertEqual(actual_output, expected_output)

    def test_is_after_thingspeak_timestamp(self):
        self.assertFalse(self.thingspk_ts2.is_after(self.thingspk_ts1))
        self.assertTrue(self.thingspk_ts1.is_after(self.thingspk_ts2))

    def test_is_same_day_thingspeak_timestamp(self):
        self.assertTrue(self.thingspk_ts1.is_same_day(self.thingspk_ts1))
        self.assertFalse(self.thingspk_ts2.is_same_day(self.thingspk_ts1))

    def test_is_after_with_different_timestamp(self):
        self.assertTrue(self.atmotube_ts1.is_after(self.thingspk_ts1))
        self.assertFalse(self.thingspk_ts1.is_after(self.atmotube_ts1))

    def test_is_after_current_timestamp(self):
        self.assertTrue(self.current_ts.is_after(self.atmotube_ts1))

    def test_unix_timestamp(self):
        self.assertEqual(self.unix_ts._ts, '2018-07-12 23:59:08')

    def test_unix_timestamp_is_after(self):
        self.assertFalse(self.unix_ts.is_after(self.atmotube_ts1))
        self.assertTrue(self.atmotube_ts1.is_after(self.unix_ts))

    def test_add_days_to_unix_timestamp(self):
        new_timest = self.unix_ts.add_days(days=10)
        actual_output = new_timest._ts
        expected_output = "2018-07-22 23:59:08"
        self.assertEqual(actual_output, expected_output)

    def test_is_same_day_current_timestamp(self):
        self.assertFalse(self.current_ts.is_same_day(self.atmotube_ts1))
        self.assertFalse(self.current_ts.is_same_day(self.unix_ts))

    def test_is_same_day_unix_timestamp(self):
        self.assertFalse(self.unix_ts.is_same_day(self.thingspk_ts1))
        self.assertTrue(self.unix_ts.is_same_day(tstype.SQLTimest(timest='2018-07-12 00:00:00')))

    def test_conversion_from_database_timestamp_to_timestamp(self):
        test_database_timestamp = dt.datetime.strptime("2021-10-11 09:44:00", tstype.SQL_TIMEST_FMT)
        actual = tstype.datetime2sqltimest(datetime_=test_database_timestamp)
        self.assertEqual(actual.ts, "2021-10-11 09:44:00")


if __name__ == '__main__':
    unittest.main()
