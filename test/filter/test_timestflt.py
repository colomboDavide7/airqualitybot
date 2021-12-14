######################################################
#
# Author: Davide Colombo
# Date: 27/11/21 17:56
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.filter.timestflt as filtertype
import airquality.api.resp.atmotube as atmtype
import airquality.types.timest as tstype


class TestTimestFilter(unittest.TestCase):

    def setUp(self) -> None:
        self.test_responses = [
            atmtype.AtmotubeAPIRespType(item={'time': "2021-10-11T08:44:00.000Z"}, measure_param=['time']),
            atmtype.AtmotubeAPIRespType(item={'time': "2021-10-11T08:46:00.000Z"}, measure_param=['time']),
            atmtype.AtmotubeAPIRespType(item={'time': "2021-10-11T08:48:00.000Z"}, measure_param=['time'])
        ]

    def test_successfully_filter_measures(self):
        test_filter_timestamp = tstype.SQLTimest(timest="2021-10-11 08:45:59")
        response_filter = filtertype.TimestFilter(timest_boundary=test_filter_timestamp)
        actual = response_filter.filter(self.test_responses)
        self.assertEqual(len(actual), 2)
        self.assertEqual(actual[0].measured_at().ts, "2021-10-11 08:46:00")
        self.assertEqual(actual[1].measured_at().ts, "2021-10-11 08:48:00")

    def test_output_empty_list(self):
        test_filter_timestamp = tstype.SQLTimest(timest="2021-10-11 08:50:00")
        response_filter = filtertype.TimestFilter(timest_boundary=test_filter_timestamp)
        actual = response_filter.filter(all_resp=self.test_responses)
        self.assertEqual(len(actual), 0)

    def test_same_output_as_input(self):
        test_filter_timestamp = tstype.SQLTimest(timest="2021-10-11 08:43:00")
        response_filter = filtertype.TimestFilter(timest_boundary=test_filter_timestamp)
        actual = response_filter.filter(all_resp=self.test_responses)
        self.assertEqual(actual, self.test_responses)

    def test_reverse_responses(self):
        test_responses = [
            atmtype.AtmotubeAPIRespType(item={'time': "2021-10-11T08:48:00.000Z"}, measure_param=['time']),
            atmtype.AtmotubeAPIRespType(item={'time': "2021-10-11T08:46:00.000Z"}, measure_param=['time']),
            atmtype.AtmotubeAPIRespType(item={'time': "2021-10-11T08:44:00.000Z"}, measure_param=['time'])
        ]
        test_filter_timestamp = tstype.SQLTimest(timest="2021-10-11 08:48:00")
        response_filter = filtertype.TimestFilter(timest_boundary=test_filter_timestamp)
        actual = response_filter.filter(all_resp=test_responses)
        self.assertEqual(len(actual), 0)


if __name__ == '__main__':
    unittest.main()
