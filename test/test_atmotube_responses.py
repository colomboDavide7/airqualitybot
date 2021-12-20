######################################################
#
# Author: Davide Colombo
# Date: 20/12/21 12:32
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch
from airquality.response import AtmotubeResponses

SQL_DATETIME_FMT = "%Y-%m-%d %H:%M:%S"
TEST_ATMOTUBE_RESPONSES = """
{
    "data": {
        "items": [
            {"time": "2021-08-10T23:59:00.000Z",
             "voc": 0.17, "pm1": 8, "pm25": 10, "pm10": 11, "t": 29, "h": 42, "p": 1004.68},
             {"time": "2021-08-11T00:00:00.000Z", 
             "voc": 0.17, "pm1": 7,"pm25": 9, "pm10": 10, "t": 29, "h": 42, "p": 1004.72, "coords": {"lat": 45, "lon": 9}}
        ]
    }
}
"""

TEST_ATMOTUBE_EMPTY_RESPONSES = """
{
"data": {
    "items": []
    }
}
"""


class TestResponses(unittest.TestCase):

    @patch('airquality.response.urlopen')
    def test_atmotube_responses_only_after_filter_datetime(self, mocked_urlopen):
        mocked_resp = MagicMock()
        mocked_resp.read.side_effect = [TEST_ATMOTUBE_RESPONSES]
        mocked_resp.getcode.return_value = 200
        mocked_resp.__enter__.return_value = mocked_resp
        mocked_urlopen.return_value = mocked_resp

        filter_datetime = datetime.strptime("2021-08-10 23:59:00", SQL_DATETIME_FMT)
        responses = AtmotubeResponses(url="some_url", filter_ts=filter_datetime)
        self.assertEqual(len(responses), 1)
        resp = responses[0]
        self.assertEqual(resp.measured_at, "2021-08-11 00:00:00")
        expected_values = [('voc', 0.17), ('pm1', 7), ('pm25', 9), ('pm10', 10), ('t', 29), ('h', 42), ('p', 1004.72)]
        self.assertEqual(resp.values, expected_values)
        self.assertEqual(resp.located_at, "ST_GeomFromText('POINT(9 45)', 26918)")

    @patch('airquality.response.urlopen')
    def test_empty_atmotube_responses(self, mocked_urlopen):
        mocked_resp = MagicMock()
        mocked_resp.getcode.return_value = 200
        mocked_resp.read.side_effect = [TEST_ATMOTUBE_EMPTY_RESPONSES]
        mocked_resp.__enter__.return_value = mocked_resp
        mocked_urlopen.return_value = mocked_resp

        filter_datetime = datetime.now()
        responses = AtmotubeResponses(url="https://foo.com", filter_ts=filter_datetime)
        self.assertEqual(len(responses), 0)

        with self.assertRaises(IndexError):
            print("IndexError caught successfully")
            responses[0]


if __name__ == '__main__':
    unittest.main()
