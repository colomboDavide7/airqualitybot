######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 14/11/21 17:25
# Description: INSERT HERE THE DESCRIPTION
#
######################################################

import unittest
import airquality.bot.util.datelooper as loop
import airquality.api.util.url as url
import airquality.database.util.datatype.timestamp as ts


class TestLooper(unittest.TestCase):

    def setUp(self) -> None:
        self.atmotube_builder = url.AtmotubeURL(address='some_address',
                                                url_param={'p1': 'v1', 'api_key': 'some_key', 'mac': 'some_mac'})
        self.thingspeak_builder = url.ThingspeakURL(address='some_address',
                                                    url_param={'format': 'json', 'channel_id': 'some_id',
                                                               'api_key': 'some_key', 'opt': 'val'})

    def test_atmotube_date_looper(self):
        test_start = ts.SQLTimestamp('2021-10-11 20:45:00')
        test_end = ts.SQLTimestamp('2021-10-12 08:22:00')
        looper = loop.AtmotubeDateLooper(url_builder=self.atmotube_builder, start_ts=test_start, stop_ts=test_end)
        actual_output = looper.get_next_url()
        expected_output = "some_address?p1=v1&api_key=some_key&mac=some_mac&date=2021-10-11"
        self.assertEqual(actual_output, expected_output)
        self.assertFalse(looper.ended)

        # Test another url
        actual_output = looper.get_next_url()
        expected_output = "some_address?p1=v1&api_key=some_key&mac=some_mac&date=2021-10-12"
        self.assertEqual(actual_output, expected_output)
        self.assertTrue(looper.ended)

        # Get another data after data is ended
        self.assertIsNone(looper.get_next_url())

    def test_thingspeak_date_looper(self):
        test_start = ts.SQLTimestamp('2021-10-11 20:45:00')
        test_end = ts.SQLTimestamp('2021-10-12 08:22:00')
        looper = loop.ThingspeakDateLooper(url_builder=self.thingspeak_builder, start_ts=test_start, stop_ts=test_end)

        actual_output = looper.get_next_url()
        expected_output = "some_address/some_id/feeds.json?api_key=some_key&opt=val&start=2021-10-11%2020:45:00&end=2021-10-12%2008:22:00"
        self.assertEqual(actual_output, expected_output)
        self.assertTrue(looper.ended)

        # Get another data after data is ended
        self.assertIsNone(looper.get_next_url())


if __name__ == '__main__':
    unittest.main()
