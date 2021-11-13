#################################################
#
# @Author: davidecolombo
# @Date: ven, 22-10-2021, 12:07
# @Description: unit test script
#
#################################################
import unittest
import airquality.database.util.timest as tsmp


class TestTimestampBuilder(unittest.TestCase):

    def setUp(self) -> None:
        self.atmotube_ts1 = tsmp.SQLTimestamp("2021-10-11T09:44:00.000Z", fmt=tsmp.ATMOTUBE_FMT)
        self.atmotube_ts2 = tsmp.SQLTimestamp("2018-01-01T00:00:00.000Z", fmt=tsmp.ATMOTUBE_FMT)
        self.thingspk_ts1 = tsmp.SQLTimestamp("2021-09-04T17:35:44Z", fmt=tsmp.THINGSPK_FMT)
        self.thingspk_ts2 = tsmp.SQLTimestamp("2020-07-14T14:05:09Z", fmt=tsmp.THINGSPK_FMT)
        self.current_ts = tsmp.CurrentTimestamp()

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


if __name__ == '__main__':
    unittest.main()
