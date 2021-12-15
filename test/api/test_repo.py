######################################################
#
# Author: Davide Colombo
# Date: 15/12/21 12:04
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
from math import ceil, floor
from unittest.mock import Mock, patch
import airquality.api.api_repo as repo
import airquality.types.timest as tstype


class TestTimeIterableURLFormatter(unittest.TestCase):

    RESPONSE = "resp"

    def test_system_exit_on_bad_url(self):
        """Test the raises of a SystemExit exception in 'fetch()' function in 'repo.api_repo.py'"""

        test_repo = repo.NTimesAPIRepo(url="bad_url")
        with self.assertRaises(SystemExit):
            next(iter(test_repo))

    @patch('airquality.api.api_repo.urlopen')
    def test_1time_api_repo(self, mocked_urlopen):
        mocked_resp = Mock()
        mocked_resp.read.return_value = self.RESPONSE
        mocked_urlopen.return_value = mocked_resp
        test_repo = repo.NTimesAPIRepo(url="some_url", ntimes=1)
        actual = iter(test_repo)
        first_response = next(actual)
        self.assertEqual(first_response, self.RESPONSE)
        with self.assertRaises(StopIteration):
            next(actual)

    @patch('airquality.api.api_repo.urlopen')
    def test_ntimes_api_repo(self, mocked_urlopen):
        test_ntimes = 3
        mocked_resp = Mock()
        mocked_resp.read.side_effect = [self.RESPONSE for _ in range(test_ntimes)]
        mocked_urlopen.return_value = mocked_resp
        test_repo = repo.NTimesAPIRepo(url="some_url", ntimes=test_ntimes)
        actual = iter(test_repo)
        for resp in actual:
            self.assertEqual(resp, self.RESPONSE)

    @patch('airquality.api.api_repo.urlopen')
    def test_1day_step_1day_time_window_atmotube_repository(self, mocked_urlopen):
        test_begin = tstype.AtmotubeSQLTimest(timest="2021-10-11T08:00:00.000Z")
        test_stop = tstype.AtmotubeSQLTimest(timest="2021-10-11T18:00:00.000Z")
        test_repo = repo.AtmotubeTimeIterableRepo(url="some_url", begin=test_begin, stop=test_stop, step_size_in_days=1)

        mocked_resp = Mock()
        mocked_resp.read.side_effect = [self.RESPONSE]
        mocked_urlopen.return_value = mocked_resp

        actual = iter(test_repo)
        for resp in actual:
            self.assertEqual(resp, self.RESPONSE)

        self.assertEqual(mocked_resp.read.call_count, 1)

    @patch('airquality.api.api_repo.urlopen')
    def test_1day_step_nday_time_window_atmotube_repository(self, mocked_urlopen):
        test_nday_step = 1
        test_begin = tstype.AtmotubeSQLTimest(timest="2021-10-11T08:00:00.000Z")
        test_stop = tstype.AtmotubeSQLTimest(timest="2021-10-22T18:00:00.000Z")
        test_repo = repo.AtmotubeTimeIterableRepo(url="some_url", begin=test_begin, stop=test_stop, step_size_in_days=test_nday_step)

        mocked_resp = Mock()
        n_cycles = ceil((22-11) / test_nday_step) + 1
        mocked_resp.read.side_effect = [self.RESPONSE for _ in range(n_cycles)]
        mocked_urlopen.return_value = mocked_resp

        actual = iter(test_repo)
        for resp in actual:
            self.assertEqual(resp, self.RESPONSE)
        self.assertEqual(mocked_resp.read.call_count, n_cycles)

    @patch('airquality.api.api_repo.urlopen')
    def test_1day_step_1day_time_window_thingspeak_repository(self, mocked_urlopen):
        test_begin = tstype.ThingspeakSQLTimest(timest="2021-10-11T08:00:00Z")
        test_stop = tstype.ThingspeakSQLTimest(timest="2021-10-11T18:00:00Z")
        test_repo = repo.ThingspeakTimeIterableAPIRepo(url="some_url", begin=test_begin, stop=test_stop, step_size_in_days=1)

        mocked_resp = Mock()
        mocked_resp.read.side_effect = [self.RESPONSE]
        mocked_urlopen.return_value = mocked_resp

        actual = iter(test_repo)
        for resp in actual:
            self.assertEqual(resp, self.RESPONSE)

        self.assertEqual(mocked_resp.read.call_count, 1)

    @patch('airquality.api.api_repo.urlopen')
    def test_nday_step_nday_time_window_thingspeak_repository(self, mocked_urlopen):
        test_nday_step = 3
        test_begin = tstype.ThingspeakSQLTimest(timest="2021-10-11T08:00:00Z")
        test_stop = tstype.ThingspeakSQLTimest(timest="2021-11-11T18:00:00Z")
        test_repo = repo.ThingspeakTimeIterableAPIRepo(url="some_url", begin=test_begin, stop=test_stop, step_size_in_days=test_nday_step)

        # from 10-11 to 11-11
        total_difference_in_days = 30
        mocked_resp = Mock()
        n_cycles = floor((total_difference_in_days / test_nday_step) + 1)
        mocked_resp.read.side_effect = [self.RESPONSE for _ in range(n_cycles)]
        mocked_urlopen.return_value = mocked_resp

        actual = iter(test_repo)
        for resp in actual:
            self.assertEqual(resp, self.RESPONSE)
        self.assertEqual(mocked_resp.read.call_count, n_cycles)


if __name__ == '__main__':
    unittest.main()
