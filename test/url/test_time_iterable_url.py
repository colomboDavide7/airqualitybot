######################################################
#
# Author: Davide Colombo
# Date: 31/12/21 14:26
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from airquality.url.timeiter_url import AtmotubeTimeIterableURL
from unittest import TestCase, main
from datetime import datetime


class TestTimeIterableURL(TestCase):

    def test_atmotube_url_formatter(self):
        test_begin = datetime.strptime('2021-12-01 00:00:00', "%Y-%m-%d %H:%M:%S")
        test_until = datetime.strptime('2021-12-03 17:44:35', "%Y-%m-%d %H:%M:%S")

        urls = AtmotubeTimeIterableURL(url="some_url", begin=test_begin, until=test_until, step_size_in_days=1)
        self.assertEqual(len(urls), 3)

        url1 = urls[0]
        self.assertEqual(url1, "some_url&date=2021-12-01")
        url2 = urls[1]
        self.assertEqual(url2, "some_url&date=2021-12-02")
        url3 = urls[2]
        self.assertEqual(url3, "some_url&date=2021-12-03")

        with self.assertRaises(IndexError):
            print(urls[3])


if __name__ == '__main__':
    main()
