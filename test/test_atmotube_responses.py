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
from airquality.response import AtmotubeResponse

SQL_DATETIME_FMT = "%Y-%m-%d %H:%M:%S"


class TestResponses(unittest.TestCase):

    @patch('airquality.response.urlopen')
    def test_atmotube_responses_only_after_filter_datetime(self, mocked_urlopen):
        with open('test_resources/atmotube_response.json') as rf:
            api_responses = rf.read()

        mocked_resp = MagicMock()
        mocked_resp.read.side_effect = [api_responses]
        mocked_resp.getcode.return_value = 200
        mocked_resp.__enter__.return_value = mocked_resp
        mocked_urlopen.return_value = mocked_resp

        filter_datetime = datetime.strptime("2021-08-10 23:59:00", SQL_DATETIME_FMT)
        responses = AtmotubeResponse(url="some_url", filter_ts=filter_datetime)
        self.assertEqual(len(responses), 1)
        resp = responses[0]
        self.assertEqual(resp.measured_at(), "2021-08-11 00:00:00")
        expected_values = {('voc', 0.17), ('pm1', 7), ('pm25', 9), ('pm10', 10), ('t', 29), ('h', 42), ('p', 1004.72)}
        self.assertEqual(resp.values(), expected_values)
        self.assertEqual(resp.located_at(), "ST_GeomFromText('POINT(9 45)', 26918)")


if __name__ == '__main__':
    unittest.main()
