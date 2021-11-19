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
import airquality.api.fetch as fetch
import airquality.api.util.extractor as ext
import airquality.file.util.parser as parse
import airquality.database.util.datatype.timestamp as ts


class TestLooper(unittest.TestCase):

    def setUp(self) -> None:
        self.atmotube_url_param = {'p1': 'v1', 'api_key': 'some_key', 'mac': 'some_mac'}
        self.atmotube_builder = url.AtmotubeURL(address='some_address', url_param=self.atmotube_url_param)
        self.atmotube_extractor = ext.AtmotubeDataExtractor()
        self.json_parser = parse.JSONParser()
        self.atmotube_fetch = fetch.FetchWrapper(
            url_builder=self.atmotube_builder,
            extractor=self.atmotube_extractor,
            parser=self.json_parser)

    ################################ ATMOTUBE DATE LOOPER ################################
    def test_single_next_atmotube_sensor_data(self):
        test_start = ts.SQLTimestamp('2021-10-11 08:45:00')
        test_end = ts.SQLTimestamp('2021-10-11 08:46:00')
        looper = loop.AtmotubeDateLooper(fetch_wrapper=self.atmotube_fetch, start_ts=test_start, stop_ts=test_end)

        # Next 1
        actual_output = looper._get_next_date_url_param()
        expected_output = {'date': '2021-10-11'}
        self.assertEqual(actual_output, expected_output)
        self.assertTrue(looper.ended)

    def test_multiple_next_atmotube_sensor_data(self):
        test_start = ts.SQLTimestamp('2021-10-11 20:45:00')
        test_end = ts.SQLTimestamp('2021-10-13 08:22:00')
        looper = loop.AtmotubeDateLooper(fetch_wrapper=self.atmotube_fetch, start_ts=test_start, stop_ts=test_end)

        # Next 1
        actual_output = looper._get_next_date_url_param()
        expected_output = {'date': '2021-10-11'}
        self.assertEqual(actual_output, expected_output)
        self.assertFalse(looper.ended)

        # Next 2
        actual_output = looper._get_next_date_url_param()
        expected_output = {'date': '2021-10-12'}
        self.assertEqual(actual_output, expected_output)
        self.assertFalse(looper.ended)

        # Next 3
        actual_output = looper._get_next_date_url_param()
        expected_output = {'date': '2021-10-13'}
        self.assertEqual(actual_output, expected_output)
        self.assertTrue(looper.ended)

    ################################ THINGSPEAK DATE LOOPER ################################
    def test_single_next_thingspeak_sensor_data(self):
        test_start = ts.SQLTimestamp('2021-10-11 08:45:00')
        test_end = ts.SQLTimestamp('2021-10-11 20:22:00')
        looper = loop.ThingspeakDateLooper(fetch_wrapper=self.atmotube_fetch, start_ts=test_start, stop_ts=test_end)

        # Next 1
        actual_output = looper._get_next_date_url_param()
        expected_output = {'start': '2021-10-11 08:45:00', 'end': '2021-10-11 20:22:00'}
        self.assertEqual(actual_output, expected_output)
        self.assertTrue(looper.ended)

    def test_multiple_next_thingspeak_sensor_data(self):
        test_start = ts.SQLTimestamp('2021-10-11 08:45:00')
        test_end = ts.SQLTimestamp('2021-11-05 20:22:00')
        looper = loop.ThingspeakDateLooper(fetch_wrapper=self.atmotube_fetch, start_ts=test_start, stop_ts=test_end)

        # Next 1
        actual_output = looper._get_next_date_url_param()
        expected_output = {'start': '2021-10-11 08:45:00', 'end': '2021-10-18 08:45:00'}
        self.assertEqual(actual_output, expected_output)
        self.assertFalse(looper.ended)

        # Next 2
        actual_output = looper._get_next_date_url_param()
        expected_output = {'start': '2021-10-18 08:45:00', 'end': '2021-10-25 08:45:00'}
        self.assertEqual(actual_output, expected_output)
        self.assertFalse(looper.ended)

        # Next 3
        actual_output = looper._get_next_date_url_param()
        expected_output = {'start': '2021-10-25 08:45:00', 'end': '2021-11-01 08:45:00'}
        self.assertEqual(actual_output, expected_output)
        self.assertFalse(looper.ended)

        # Next 4
        actual_output = looper._get_next_date_url_param()
        expected_output = {'start': '2021-11-01 08:45:00', 'end': '2021-11-05 20:22:00'}
        self.assertEqual(actual_output, expected_output)
        self.assertTrue(looper.ended)


if __name__ == '__main__':
    unittest.main()
