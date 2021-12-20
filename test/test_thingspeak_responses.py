######################################################
#
# Author: Davide Colombo
# Date: 20/12/21 15:32
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from unittest import TestCase, main
from unittest.mock import MagicMock, patch
from airquality.response import ThingspeakResponse
from datetime import datetime
from airquality.thingspeak import MAPPING_1A, MAPPING_1B, MAPPING_2A, MAPPING_2B     # importing the 'field_map'

SQL_DATETIME_FMT = "%Y-%m-%d %H:%M:%S"


class TestThingspeakResponse(TestCase):

    @patch('airquality.response.urlopen')
    def test_successfully_fetch_responses_channel1A(self, mocked_urlopen):
        with open('test_resources/thingspeak_response_1A.json') as rf:
            channel_1a_responses = rf.read()

        mocked_resp = MagicMock()
        mocked_resp.getcode.return_value = 200
        mocked_resp.read.side_effect = [channel_1a_responses]
        mocked_resp.__enter__.return_value = mocked_resp
        mocked_urlopen.return_value = mocked_resp

        filter_datetime = datetime.strptime("2021-12-20 11:20:40", SQL_DATETIME_FMT)
        response = ThingspeakResponse(url="thingspeak.com", field_map=MAPPING_1A, filter_ts=filter_datetime)
        self.assertEqual(len(response), 1)
        resp = response[0]
        self.assertEqual(resp.measured_at(), "2021-12-20 11:22:40")
        expected_values = {('pm1.0_atm_a', "30.29"), ('pm2.5_atm_a', "52.67"), ('pm10.0_atm_a', "56.11"), ('temperature_a', "55"), ('humidity_a', "59")}
        self.assertEqual(resp.values(), expected_values)

        with self.assertRaises(IndexError):
            print("IndexError caught successfully")
            response[1]

    @patch('airquality.response.urlopen')
    def test_successfully_fetch_responses_channel1B(self, mocked_urlopen):
        with open('test_resources/thingspeak_response_1B.json') as rf:
            channel_1a_responses = rf.read()

        mocked_resp = MagicMock()
        mocked_resp.getcode.return_value = 200
        mocked_resp.read.side_effect = [channel_1a_responses]
        mocked_resp.__enter__.return_value = mocked_resp
        mocked_urlopen.return_value = mocked_resp

        filter_datetime = datetime.strptime("2021-12-19 11:06:25", SQL_DATETIME_FMT)
        response = ThingspeakResponse(url="thingspeak.com", field_map=MAPPING_1B, filter_ts=filter_datetime)
        self.assertEqual(len(response), 2)
        resp = response[0]
        self.assertEqual(resp.measured_at(), "2021-12-19 11:08:25")
        expected_values = {('pm1.0_atm_b', "125.93"), ('pm2.5_atm_b', "227.33"), ('pm10.0_atm_b', "287.29"), ('pressure_b', "1016.44")}
        self.assertEqual(resp.values(), expected_values)

        resp = response[1]
        self.assertEqual(resp.measured_at(), "2021-12-19 11:10:25")
        expected_values = {('pm1.0_atm_b', "125.72"), ('pm2.5_atm_b', "216.91"), ('pm10.0_atm_b', "272.86"), ('pressure_b', "1016.38")}
        self.assertEqual(resp.values(), expected_values)

        with self.assertRaises(IndexError):
            print("IndexError caught successfully")
            response[2]

    @patch('airquality.response.urlopen')
    def test_successfully_fetch_responses_channel2A(self, mocked_urlopen):
        with open('test_resources/thingspeak_response_2A.json') as rf:
            channel_1a_responses = rf.read()

        mocked_resp = MagicMock()
        mocked_resp.getcode.return_value = 200
        mocked_resp.read.side_effect = [channel_1a_responses]
        mocked_resp.__enter__.return_value = mocked_resp
        mocked_urlopen.return_value = mocked_resp

        filter_datetime = datetime.strptime("2021-12-19 11:06:23", SQL_DATETIME_FMT)
        response = ThingspeakResponse(url="thingspeak.com", field_map=MAPPING_2A, filter_ts=filter_datetime)
        self.assertEqual(len(response), 1)
        resp = response[0]
        self.assertEqual(resp.measured_at(), "2021-12-19 11:08:23")
        expected_values = {('0.3_um_count_a', "10676.61"), ('0.5_um_count_a', "3037.76"), ('1.0_um_count_a', "744.85"),
                           ('2.5_um_count_a', "122.69"), ('5.0_um_count_a', "24.39"), ('10.0_um_count_a', "0.96")}
        self.assertEqual(resp.values(), expected_values)

        with self.assertRaises(IndexError):
            print("IndexError caught successfully")
            response[1]

    @patch('airquality.response.urlopen')
    def test_successfully_fetch_responses_channel2B(self, mocked_urlopen):
        with open('test_resources/thingspeak_response_2B.json') as rf:
            channel_1a_responses = rf.read()

        mocked_resp = MagicMock()
        mocked_resp.getcode.return_value = 200
        mocked_resp.read.side_effect = [channel_1a_responses]
        mocked_resp.__enter__.return_value = mocked_resp
        mocked_urlopen.return_value = mocked_resp

        filter_datetime = datetime.strptime("2021-12-09 15:54:34", SQL_DATETIME_FMT)
        response = ThingspeakResponse(url="thingspeak.com", field_map=MAPPING_2B, filter_ts=filter_datetime)
        self.assertEqual(len(response), 1)
        resp = response[0]
        self.assertEqual(resp.measured_at(), "2021-12-09 15:56:34")
        expected_values = {('0.3_um_count_b', "5535.57"), ('0.5_um_count_b', "1661.58"), ('1.0_um_count_b', "302.30"),
                           ('2.5_um_count_b', "44.28"), ('5.0_um_count_b', "7.64"), ('10.0_um_count_b', "0.98")}
        self.assertEqual(resp.values(), expected_values)

        with self.assertRaises(IndexError):
            print("IndexError caught successfully")
            response[1]


if __name__ == '__main__':
    main()
