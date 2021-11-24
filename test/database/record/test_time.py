######################################################
#
# Author: Davide Colombo
# Date: 16/11/21 12:22
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import database.rec.timerec as t
import database.dtype.timestamp as ts
import airquality.adapter.config as adapt_const
import database.dtype.config as time_conf


class TestTimeRecord(unittest.TestCase):

    def setUp(self) -> None:
        self.time_rec = t.TimeRecord()

    def test_time_record_with_atmotube_timestamp_class(self):
        test_data = {adapt_const.TIMEST: {adapt_const.CLS: ts.AtmotubeTimestamp,
                                          adapt_const.KW: {time_conf.TIMEST_INIT_TIMESTAMP: '2018-10-11T09:44:00.000Z'}}}
        actual_output = self.time_rec.record(test_data)
        expected_output = f"'2018-10-11 09:44:00'"
        self.assertEqual(actual_output, expected_output)

    def test_time_record_with_thingspeak_timestamp_class(self):
        test_data = {adapt_const.TIMEST: {adapt_const.CLS: ts.ThingspeakTimestamp,
                                          adapt_const.KW: {time_conf.TIMEST_INIT_TIMESTAMP: '2018-10-11T09:44:00Z'}}}
        actual_output = self.time_rec.record(test_data)
        expected_output = f"'2018-10-11 09:44:00'"
        self.assertEqual(actual_output, expected_output)

    def test_exit_on_missing_timestamp(self):
        bad_data = {'bad': 'val'}
        with self.assertRaises(SystemExit):
            self.time_rec.record(bad_data)

    def test_exit_on_missing_class_or_kwargs(self):
        test_data = {adapt_const.TIMEST: {adapt_const.KW: {time_conf.TIMEST_INIT_TIMESTAMP: '2018-10-11T09:44:00Z'}}}
        with self.assertRaises(SystemExit):
            self.time_rec.record(test_data)

        test_data = {adapt_const.TIMEST: {adapt_const.CLS: ts.ThingspeakTimestamp}}
        with self.assertRaises(SystemExit):
            self.time_rec.record(test_data)

    def test_exit_on_empty_timestamp_dictionary(self):
        test_data = {adapt_const.TIMEST: {}}
        with self.assertRaises(SystemExit):
            self.time_rec.record(test_data)


if __name__ == '__main__':
    unittest.main()
