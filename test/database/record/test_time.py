######################################################
#
# Author: Davide Colombo
# Date: 16/11/21 12:22
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.database.util.record.time as t
import airquality.database.util.datatype.timestamp as ts


class TestTimeRecord(unittest.TestCase):

    def setUp(self) -> None:
        self.atmotube_ts_class = ts.AtmotubeTimestamp
        self.thingspeak_ts_class = ts.ThingspeakTimestamp
        self.atmotube_time_rec = t.TimeRecord(self.atmotube_ts_class)
        self.thingspeak_time_rec = t.TimeRecord(self.thingspeak_ts_class)

    def test_time_record_with_atmotube_timestamp_class(self):
        test_data = {'timestamp': '2018-10-11T09:44:00.000Z'}
        actual_output = self.atmotube_time_rec.record(test_data)
        expected_output = f"'2018-10-11 09:44:00'"
        self.assertEqual(actual_output, expected_output)

    def test_time_record_with_thingspeak_timestamp_class(self):
        test_data = {'timestamp': '2018-10-11T09:44:00Z'}
        actual_output = self.thingspeak_time_rec.record(test_data)
        expected_output = f"'2018-10-11 09:44:00'"
        self.assertEqual(actual_output, expected_output)

    def test_exit_on_missing_timestamp(self):
        bad_data = {'bad': 'val'}
        with self.assertRaises(SystemExit):
            self.atmotube_time_rec.record(bad_data)

        with self.assertRaises(SystemExit):
            self.thingspeak_time_rec.record(bad_data)


if __name__ == '__main__':
    unittest.main()
