######################################################
#
# Author: Davide Colombo
# Date: 27/11/21 10:29
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import api as privateurl
import api as urltype
import airquality.types.timestamp as tstype


class TestTimeIterableURL(unittest.TestCase):

    def setUp(self) -> None:
        atmotube_template = "some_address?api_key={api_key}&mac={mac}&order=asc&format={fmt}"
        self.atmotube_url = privateurl.AtmotubeURLBuilder(url_template=atmotube_template, api_key="some_key", ident="ident", fmt="fmt")

        thingspeak_template = "some_address/{channel_id}/feeds.{fmt}?api_key={api_key}"
        self.thingspeak_url = privateurl.ThingspeakURLBuilder(url_template=thingspeak_template, api_key="some_key", ident="ident", fmt="fmt")

    ################################ ATMOTUBE URL TIME DECORATOR ###############################
    def test_successfully_decorate_atmotube_url_with_multiple_days_time_window(self):
        start = tstype.SQLTimestamp(timest='2021-10-11 08:45:00')
        stop = tstype.SQLTimestamp(timest='2021-10-13 20:45:00')
        iterable_url = urltype.AtmotubeTimeIterableURL(url=self.atmotube_url, step_size_in_days=1, start_ts=start, stop_ts=stop)
        generator = iterable_url.build()

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
        start = tstype.SQLTimestamp(timest='2021-10-11 08:45:00')
        stop = tstype.SQLTimestamp(timest='2021-10-11 20:45:00')
        iterable_url = urltype.AtmotubeTimeIterableURL(url=self.atmotube_url, step_size_in_days=1, start_ts=start, stop_ts=stop)
        generator = iterable_url.build()

        actual = next(generator)
        expected = "some_address?api_key=some_key&mac=ident&order=asc&format=fmt&date=2021-10-11"
        self.assertEqual(actual, expected)

        with self.assertRaises(StopIteration):
            next(generator)

    ################################ THINGSPEAK URL TIME DECORATOR ###############################
    def test_successfully_decorate_thingspeak_url_with_multiple_days_time_window(self):
        start = tstype.SQLTimestamp(timest='2021-10-11 08:45:00')
        stop = tstype.SQLTimestamp(timest='2021-11-07 20:45:00')
        iterable_url = urltype.ThingspeakTimeIterableURL(url=self.thingspeak_url, step_size_in_days=7, start_ts=start, stop_ts=stop)
        generator = iterable_url.build()

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
        start = tstype.SQLTimestamp(timest='2021-11-11 08:45:00')
        stop = tstype.SQLTimestamp(timest='2021-11-11 20:45:00')
        iterable_url = urltype.ThingspeakTimeIterableURL(url=self.thingspeak_url, step_size_in_days=7, start_ts=start, stop_ts=stop)
        generator = iterable_url.build()

        actual = next(generator)
        expected = "some_address/ident/feeds.fmt?api_key=some_key&start=2021-11-11%2008:45:00&end=2021-11-11%2020:45:00"
        self.assertEqual(actual, expected)

        with self.assertRaises(StopIteration):
            next(generator)


if __name__ == '__main__':
    unittest.main()
