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
import airquality.adapter.config as c


class TestTimeRecord(unittest.TestCase):

    def setUp(self) -> None:
        self.time_rec = t.TimeRecord()

    def test_time_record_with_atmotube_timestamp_class(self):
        test_data = {c.TIMEST: {c.CLS: ts.AtmotubeTimestamp, c.KW: {'timestamp': '2018-10-11T09:44:00.000Z'}}}
        actual_output = self.time_rec.record(test_data)
        expected_output = f"'2018-10-11 09:44:00'"
        self.assertEqual(actual_output, expected_output)

    def test_time_record_with_thingspeak_timestamp_class(self):
        test_data = {c.TIMEST: {c.CLS: ts.ThingspeakTimestamp, c.KW: {'timestamp': '2018-10-11T09:44:00Z'}}}
        actual_output = self.time_rec.record(test_data)
        expected_output = f"'2018-10-11 09:44:00'"
        self.assertEqual(actual_output, expected_output)

    def test_exit_on_missing_timestamp(self):
        bad_data = {'bad': 'val'}
        with self.assertRaises(SystemExit):
            self.time_rec.record(bad_data)

    def test_exit_on_missing_class_or_kwargs(self):
        test_data = {c.TIMEST: {c.KW: {'timestamp': '2018-10-11T09:44:00Z'}}}
        with self.assertRaises(SystemExit):
            self.time_rec.record(test_data)

        test_data = {c.TIMEST: {c.CLS: ts.ThingspeakTimestamp}}
        with self.assertRaises(SystemExit):
            self.time_rec.record(test_data)

    def test_exit_on_empty_timestamp_dictionary(self):
        test_data = {c.TIMEST: {}}
        with self.assertRaises(SystemExit):
            self.time_rec.record(test_data)


if __name__ == '__main__':
    unittest.main()
