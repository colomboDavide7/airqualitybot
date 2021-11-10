#################################################
#
# @Author: davidecolombo
# @Date: ven, 22-10-2021, 12:07
# @Description: unit test script
#
#################################################
import unittest
import airquality.data.builder.timest as tsmp


class TestTimestampBuilder(unittest.TestCase):

    def setUp(self) -> None:
        self.atmotube_ts1 = tsmp.AtmotubeTimestamp("2021-10-11T09:44:00.000Z")
        self.atmotube_ts2 = tsmp.AtmotubeTimestamp("2018-01-01T00:00:00.000Z")
        self.thingspk_ts1 = tsmp.ThingspeakTimestamp("2021-09-04T17:35:44Z")
        self.thingspk_ts2 = tsmp.ThingspeakTimestamp("2020-07-14T14:05:09Z")

    def test_successfully_add_days_to_atmotube_timestamp(self):
        new_timest = self.atmotube_ts1.add_days(days=1)
        actual_output = new_timest.ts
        expected_output = "2021-10-12 09:44:00"
        self.assertEqual(actual_output, expected_output)

    def test_is_after_atmotube_timestamp(self):
        self.assertFalse(self.atmotube_ts2.is_after(self.atmotube_ts1))
        self.assertTrue(self.atmotube_ts1.is_after(self.atmotube_ts2))

    def test_system_exit_when_comparing_bad_type(self):
        with self.assertRaises(SystemExit):
            self.atmotube_ts1.is_after(self.thingspk_ts1)

    def test_system_exit_when_using_wrong_atmotube_timestamp_fmt(self):
        with self.assertRaises(SystemExit):
            tsmp.AtmotubeTimestamp(timestamp="bad timestamp fmt")

    def test_successfully_add_days_to_thingspeak_timestamp(self):
        new_timest = self.thingspk_ts1.add_days(days=10)
        actual_output = new_timest.ts
        expected_output = "2021-09-14 17:35:44"
        self.assertEqual(actual_output, expected_output)

    def test_is_before_thingspeak_timestamp(self):
        self.assertFalse(self.thingspk_ts2.is_after(self.thingspk_ts1))
        self.assertTrue(self.thingspk_ts1.is_after(self.thingspk_ts2))

    def test_system_exit_when_using_wrong_thingspeak_timestamp_fmt(self):
        with self.assertRaises(SystemExit):
            tsmp.ThingspeakTimestamp(timestamp="bad timestamp fmt")

    def test_system_exit_when_comparing_thingspeak_timestamp_to_invalid_type(self):
        with self.assertRaises(SystemExit):
            self.thingspk_ts1.is_after(self.atmotube_ts1)

    def test_not_implemented_error_on_current_timestamp(self):
        with self.assertRaises(NotImplementedError):
            tsmp.CurrentTimestamp().add_days(days=1)

        with self.assertRaises(NotImplementedError):
            tsmp.CurrentTimestamp().is_after(self.atmotube_ts1)


if __name__ == '__main__':
    unittest.main()
