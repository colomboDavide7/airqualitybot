######################################################
#
# Author: Davide Colombo
# Date: 27/11/21 17:56
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.filter.tsfilt as flt
import airquality.types.apiresp.measresp as resp
import airquality.types.timestamp as ts


class TestTimestampFilter(unittest.TestCase):

    def setUp(self) -> None:
        self.test_responses = [
            resp.MeasureAPIResp(timestamp=ts.SQLTimestamp(timest="2021-10-11 08:44:00"), measures=[]),
            resp.MeasureAPIResp(timestamp=ts.SQLTimestamp(timest="2021-10-11 08:46:00"), measures=[]),
            resp.MeasureAPIResp(timestamp=ts.SQLTimestamp(timest="2021-10-11 08:48:00"), measures=[])
        ]

    def test_successfully_filter_measures_before_filter_timestamp(self):
        test_filter_timestamp = ts.SQLTimestamp(timest="2021-10-11 08:45:00")
        resp_filter = flt.TimestampFilter()
        resp_filter.set_filter_ts(test_filter_timestamp)
        actual = resp_filter.filter(resp2filter=self.test_responses)
        self.assertEqual(len(actual), 2)
        self.assertEqual(actual[0].timestamp.ts, "2021-10-11 08:46:00")
        self.assertEqual(actual[1].timestamp.ts, "2021-10-11 08:48:00")

    def test_empty_list_when_all_measures_are_before_filter_timestamp(self):
        test_filter_timestamp = ts.SQLTimestamp(timest="2021-10-11 08:50:00")
        resp_filter = flt.TimestampFilter()
        resp_filter.set_filter_ts(test_filter_timestamp)
        actual = resp_filter.filter(resp2filter=self.test_responses)
        self.assertEqual(len(actual), 0)

    def test_system_exit_when_filter_timestamp_is_null_timestamp(self):
        resp_filter = flt.TimestampFilter()
        with self.assertRaises(SystemExit):
            resp_filter.filter(resp2filter=self.test_responses)


if __name__ == '__main__':
    unittest.main()
