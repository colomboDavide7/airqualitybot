######################################################
#
# Author: Davide Colombo
# Date: 27/11/21 10:29
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.api.url.timeiter as urldec
import airquality.types.timestamp as ts


class TestTimeIterableURL(unittest.TestCase):

    def setUp(self) -> None:
        self.test_atm_url_template = "some_address?api_key={api_key}&mac={mac}&order=asc&format={fmt}"
        self.atm_iterable_url = urldec.AtmotubeTimeIterableURL(url_template=self.test_atm_url_template, step_size_in_days=1)
        self.atm_iterable_url.with_identifier('ident').with_api_key('some_key').with_api_response_fmt("fmt")

        self.test_thnk_url_template = "some_address/{channel_id}/feeds.{fmt}?api_key={api_key}"
        self.thnk_iterable_url = urldec.ThingspeakTimeIterableURL(url_template=self.test_thnk_url_template, step_size_in_days=7)
        self.thnk_iterable_url.with_identifier('ident').with_api_key('some_key').with_api_response_fmt("fmt")

    ################################ ATMOTUBE URL TIME DECORATOR ###############################
    def test_successfully_decorate_atmotube_url_with_multiple_days_time_window(self):
        test_start_ts = ts.SQLTimestamp(timest='2021-10-11 08:45:00')
        test_stop_ts = ts.SQLTimestamp(timest='2021-10-13 20:45:00')

        self.atm_iterable_url.with_url_time_param_template().from_(start=test_start_ts).to_(stop=test_stop_ts)

        generator = self.atm_iterable_url.build()

        actual = next(generator)
        expected = "some_address?api_key=some_key&mac=ident&order=asc&format=fmt&date=2021-10-11"
        self.assertEqual(actual, expected)

        actual = next(generator)
        expected = "some_address?api_key=some_key&mac=ident&order=asc&format=fmt&date=2021-10-12"
        self.assertEqual(actual, expected)

        actual = next(generator)
        expected = "some_address?api_key=some_key&mac=ident&order=asc&format=fmt&date=2021-10-13"
        self.assertEqual(actual, expected)

        with self.assertRaises(StopIteration):
            next(generator)

    def test_successfully_decorate_atmotube_url_with_single_day_time_window(self):
        test_start_ts = ts.SQLTimestamp(timest='2021-10-11 08:45:00')
        test_stop_ts = ts.SQLTimestamp(timest='2021-10-11 20:45:00')

        self.atm_iterable_url.with_url_time_param_template().from_(start=test_start_ts).to_(stop=test_stop_ts)
        generator = self.atm_iterable_url.build()

        actual = next(generator)
        expected = "some_address?api_key=some_key&mac=ident&order=asc&format=fmt&date=2021-10-11"
        self.assertEqual(actual, expected)

        with self.assertRaises(StopIteration):
            next(generator)

    ################################ THINGSPEAK URL TIME DECORATOR ###############################
    def test_successfully_decorate_thingspeak_url_with_multiple_days_time_window(self):
        test_start_ts = ts.SQLTimestamp(timest='2021-10-11 08:45:00')
        test_stop_ts = ts.SQLTimestamp(timest='2021-11-07 20:45:00')

        self.thnk_iterable_url.with_url_time_param_template().from_(start=test_start_ts).to_(stop=test_stop_ts)

        generator = self.thnk_iterable_url.build()
        actual = next(generator)
        expected = "some_address/ident/feeds.fmt?api_key=some_key&start=2021-10-11%2008:45:00&end=2021-10-18%2008:45:00"
        self.assertEqual(actual, expected)

        actual = next(generator)
        expected = "some_address/ident/feeds.fmt?api_key=some_key&start=2021-10-18%2008:45:00&end=2021-10-25%2008:45:00"
        self.assertEqual(actual, expected)

        actual = next(generator)
        expected = "some_address/ident/feeds.fmt?api_key=some_key&start=2021-10-25%2008:45:00&end=2021-11-01%2008:45:00"
        self.assertEqual(actual, expected)

        actual = next(generator)
        expected = "some_address/ident/feeds.fmt?api_key=some_key&start=2021-11-01%2008:45:00&end=2021-11-07%2020:45:00"
        self.assertEqual(actual, expected)

        with self.assertRaises(StopIteration):
            next(generator)

    def test_successfully_decorate_thingspeak_url_with_single_day_time_window(self):
        test_start_ts = ts.SQLTimestamp(timest='2021-11-11 08:45:00')
        test_stop_ts = ts.SQLTimestamp(timest='2021-11-11 20:45:00')

        self.thnk_iterable_url.with_url_time_param_template().from_(start=test_start_ts).to_(stop=test_stop_ts)
        generator = self.thnk_iterable_url.build()
        actual = next(generator)
        expected = "some_address/ident/feeds.fmt?api_key=some_key&start=2021-11-11%2008:45:00&end=2021-11-11%2020:45:00"
        self.assertEqual(actual, expected)

        with self.assertRaises(StopIteration):
            next(generator)

    # ################################ TEST ERRORS OR BORDER LINE CASES ###############################
    # def test_system_exit_when_decorate_thingspeak_url_without_time_window(self):
    #     decorator = urldec.ThingspeakTimeIterableURL(url=self.test_thnk_url, step_size_in_days=7)
    #     with self.assertRaises(SystemExit):
    #         decorator.build()
    #
    # def test_system_exit_when_decorate_atmotube_url_without_time_window(self):
    #     decorator = urldec.AtmotubeTimeIterableURL(url=self.test_atm_url, step_size_in_days=1)
    #     with self.assertRaises(SystemExit):
    #         decorator.build()


if __name__ == '__main__':
    unittest.main()
