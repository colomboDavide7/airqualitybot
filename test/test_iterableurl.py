######################################################
#
# Author: Davide Colombo
# Date: 22/12/21 17:41
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from unittest import TestCase, main
from datetime import datetime
from airquality.iterableurl import AtmotubeIterableURL, ThingspeakIterableURL

SQL_DATETIME_FMT = "%Y-%m-%d %H:%M:%S"


class TestIterableURL(TestCase):

    def test_iterate_over_atmotube_url(self):
        test_begin = datetime.strptime("2021-10-11 08:22:00", SQL_DATETIME_FMT)
        test_until = datetime.strptime("2021-10-11 20:45:00", SQL_DATETIME_FMT)
        iterable_url = AtmotubeIterableURL(url_template="some_url", begin=test_begin, until=test_until, step_in_days=1)
        urls = iter(iterable_url)
        self.assertEqual(next(urls), "some_url&date=2021-10-11")
        with self.assertRaises(StopIteration):
            next(urls)

    def test_iterate_over_multiple_days_atmotube_url(self):
        test_begin = datetime.strptime("2021-10-11 08:22:00", SQL_DATETIME_FMT)
        test_until = datetime.strptime("2021-10-13 20:45:00", SQL_DATETIME_FMT)
        iterable_url = AtmotubeIterableURL(url_template="some_url", begin=test_begin, until=test_until, step_in_days=1)
        urls = iter(iterable_url)
        self.assertEqual(next(urls), "some_url&date=2021-10-11")
        self.assertEqual(next(urls), "some_url&date=2021-10-12")
        self.assertEqual(next(urls), "some_url&date=2021-10-13")
        with self.assertRaises(StopIteration):
            next(urls)

    def test_iterate_over_thingspeak_url(self):
        test_begin = datetime.strptime("2021-10-11 08:22:00", SQL_DATETIME_FMT)
        test_until = datetime.strptime("2021-10-11 20:45:00", SQL_DATETIME_FMT)
        iterable_url = ThingspeakIterableURL(url_template="some_url", begin=test_begin, until=test_until, step_in_days=7)
        urls = iter(iterable_url)
        self.assertEqual(next(urls), "some_url&start=2021-10-11%2008:22:00&end=2021-10-11%2020:45:00")
        with self.assertRaises(StopIteration):
            next(urls)

    def test_iterate_over_multiple_days_thingspeak_url(self):
        test_begin = datetime.strptime("2021-10-11 08:22:00", SQL_DATETIME_FMT)
        test_until = datetime.strptime("2021-10-24 20:45:00", SQL_DATETIME_FMT)
        iterable_url = ThingspeakIterableURL(url_template="some_url", begin=test_begin, until=test_until, step_in_days=7)
        urls = iter(iterable_url)
        self.assertEqual(next(urls), "some_url&start=2021-10-11%2008:22:00&end=2021-10-18%2008:22:00")
        self.assertEqual(next(urls), "some_url&start=2021-10-18%2008:22:00&end=2021-10-24%2020:45:00")
        with self.assertRaises(StopIteration):
            next(urls)


if __name__ == '__main__':
    main()
