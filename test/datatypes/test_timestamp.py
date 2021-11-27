#################################################
#
# @Author: davidecolombo
# @Date: ven, 22-10-2021, 12:07
# @Description: unit test script
#
#################################################
import unittest
import airquality.types.timestamp as ts


class TestTimestampBuilder(unittest.TestCase):

    def setUp(self) -> None:
        self.atmotube_ts1 = ts.SQLTimestamp("2021-10-11T09:44:00.000Z", fmt=ts.ATMOTUBE_FMT)
        self.atmotube_ts2 = ts.SQLTimestamp("2018-01-01T00:00:00.000Z", fmt=ts.ATMOTUBE_FMT)
        self.thingspk_ts1 = ts.SQLTimestamp("2021-09-04T17:35:44Z", fmt=ts.THINGSPK_FMT)
        self.thingspk_ts2 = ts.SQLTimestamp("2020-07-14T14:05:09Z", fmt=ts.THINGSPK_FMT)
        self.current_ts = ts.CurrentTimestamp()
        self.unix_ts = ts.UnixTimestamp(timest=1531432748)
        self.null_ts = ts.NullTimestamp()

    def test_successfully_add_days_to_atmotube_timestamp(self):
        new_timest = self.atmotube_ts1.add_days(days=1)
        actual_output = new_timest.ts
        expected_output = "2021-10-12 09:44:00"
        self.assertEqual(actual_output, expected_output)

    def test_is_after_atmotube_timestamp(self):
        self.assertFalse(self.atmotube_ts2.is_after(self.atmotube_ts1))
        self.assertTrue(self.atmotube_ts1.is_after(self.atmotube_ts2))

    def test_successfully_add_days_to_thingspeak_timestamp(self):
        new_timest = self.thingspk_ts1.add_days(days=10)
        actual_output = new_timest.ts
        expected_output = "2021-09-14 17:35:44"
        self.assertEqual(actual_output, expected_output)

    def test_is_after_thingspeak_timestamp(self):
        self.assertFalse(self.thingspk_ts2.is_after(self.thingspk_ts1))
        self.assertTrue(self.thingspk_ts1.is_after(self.thingspk_ts2))

    def test_is_after_with_different_timestamp(self):
        self.assertTrue(self.atmotube_ts1.is_after(self.thingspk_ts1))
        self.assertFalse(self.thingspk_ts1.is_after(self.atmotube_ts1))

    def test_is_after_current_timestamp(self):
        self.assertTrue(self.current_ts.is_after(self.atmotube_ts1))

    def test_unix_timestamp(self):
        self.assertEqual(self.unix_ts.ts, '2018-07-12 23:59:08')

    def test_unix_timestamp_is_after(self):
        self.assertFalse(self.unix_ts.is_after(self.atmotube_ts1))
        self.assertTrue(self.atmotube_ts1.is_after(self.unix_ts))

    def test_add_day_to_unix_timestamp(self):
        new_timest = self.unix_ts.add_days(days=10)
        actual_output = new_timest.ts
        expected_output = "2018-07-22 23:59:08"
        self.assertEqual(actual_output, expected_output)

    def test_is_same_day_atmotube_timestamp(self):
        self.assertTrue(self.atmotube_ts1.is_same_day(self.atmotube_ts1))
        self.assertFalse(self.atmotube_ts1.is_same_day(self.atmotube_ts2))

    def test_is_same_day_thingspeak_timestamp(self):
        self.assertTrue(self.thingspk_ts1.is_same_day(self.thingspk_ts1))
        self.assertFalse(self.thingspk_ts2.is_same_day(self.thingspk_ts1))

    def test_is_same_day_current_timestamp(self):
        self.assertFalse(self.current_ts.is_same_day(self.atmotube_ts1))
        self.assertFalse(self.current_ts.is_same_day(self.unix_ts))

    def test_is_same_day_unix_timestamp(self):
        self.assertFalse(self.unix_ts.is_same_day(self.thingspk_ts1))
        self.assertTrue(self.unix_ts.is_same_day(ts.SQLTimestamp(timest='2018-07-12 00:00:00')))

    def test_null_timestamp_object(self):
        self.assertEqual(self.null_ts.ts, "NULL")

    def test_system_exit_when_comparing_null_timestamp(self):
        with self.assertRaises(SystemExit):
            self.null_ts.is_after(self.unix_ts)

    def test_system_exit_when_add_days_to_null_timestamp(self):
        with self.assertRaises(SystemExit):
            self.null_ts.add_days(100)


if __name__ == '__main__':
    unittest.main()
