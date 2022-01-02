######################################################
#
# Author: Davide Colombo
# Date: 29/12/21 20:06
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from unittest import TestCase, main
from unittest.mock import MagicMock, patch
from airquality.core.apidata_builder import PurpleairAPIDataBuilder, AtmotubeAPIDataBuilder, ThingspeakAPIDataBuilder, \
    GeonamesDataBuilder


class TestDatamodelBuilder(TestCase):

    ##################################### test_create_purpleair_datamodel #####################################
    @patch('airquality.core.apidata_builder.urlopen')
    def test_create_purpleair_datamodel(self, mocked_urlopen):
        with open('test_resources/purpleair_response.json', 'r') as rf:
            test_api_responses = rf.read()

        mocked_resp = MagicMock()
        mocked_resp.read.side_effect = [test_api_responses]
        mocked_resp.__enter__.return_value = mocked_resp
        mocked_urlopen.return_value = mocked_resp

        requests = PurpleairAPIDataBuilder(url="fake_url")
        self.assertEqual(len(requests), 3)
        req1 = requests[0]
        self.assertEqual(req1.name, "n1")
        self.assertEqual(req1.sensor_index, 1)
        self.assertEqual(req1.latitude, 45.29)
        self.assertEqual(req1.longitude, 9.13)
        self.assertEqual(req1.altitude, 274)
        self.assertEqual(req1.primary_id_a, 111)
        self.assertEqual(req1.primary_key_a, "key1a1")
        self.assertEqual(req1.primary_id_b, 112)
        self.assertEqual(req1.primary_key_b, "key1b1")
        self.assertEqual(req1.secondary_id_a, 113)
        self.assertEqual(req1.secondary_key_a, "key2a1")
        self.assertEqual(req1.secondary_id_b, 114)
        self.assertEqual(req1.secondary_key_b, "key2b1")
        self.assertEqual(req1.date_created, 1531432748)

        with self.assertRaises(IndexError):
            print(requests[3])

        with self.assertRaises(IndexError):
            print(requests[-4])

    ##################################### test_create_atmotube_datamodel #####################################
    @patch('airquality.core.apidata_builder.urlopen')
    def test_create_atmotube_datamodel(self, mocked_urlopen):
        with open('test_resources/atmotube_response.json', 'r') as rf:
            test_api_responses = rf.read()

        mocked_resp = MagicMock()
        mocked_resp.read.side_effect = [test_api_responses]
        mocked_resp.__enter__.return_value = mocked_resp
        mocked_urlopen.return_value = mocked_resp

        requests = AtmotubeAPIDataBuilder(url="fake_url")
        self.assertEqual(len(requests), 2)
        req1 = requests[0]
        self.assertEqual(req1.time, "2021-08-10T23:59:00.000Z")
        self.assertEqual(req1.voc, 0.17)
        self.assertEqual(req1.pm1, 8)
        self.assertEqual(req1.pm25, 10)
        self.assertEqual(req1.pm10, 11)
        self.assertEqual(req1.t, 29)
        self.assertEqual(req1.h, 42)
        self.assertEqual(req1.p, 1004.68)

        with self.assertRaises(IndexError):
            print(requests[2])

        with self.assertRaises(IndexError):
            print(requests[-3])

    ##################################### test_create_atmotube_datamodel #####################################
    @patch('airquality.core.apidata_builder.urlopen')
    def test_create_thingspeak_primary_channel_a_data(self, mocked_urlopen):
        with open('test_resources/thingspeak_response_1A.json', 'r') as rf:
            api_responses = rf.read()

        mocked_resp = MagicMock()
        mocked_resp.read.side_effect = [api_responses]
        mocked_resp.__enter__.return_value = mocked_resp
        mocked_urlopen.return_value = mocked_resp

        apidata = ThingspeakAPIDataBuilder(url="fake_url")
        self.assertEqual(len(apidata), 3)
        data = apidata[0]
        self.assertEqual(data.field1, 20.50)
        self.assertEqual(data.field2, 35.53)
        self.assertEqual(data.field3, 37.43)
        self.assertEqual(data.field6, 55)
        self.assertEqual(data.field7, 60)

    @patch('airquality.core.apidata_builder.open')
    def test_create_geonames_spain_data(self, mocked_open):
        with open('test_resources/ES.txt') as rf:
            spain_data = rf.read()

        mocked_responses = MagicMock()
        mocked_responses.read.side_effect = [spain_data]
        mocked_responses.__enter__.return_value = mocked_responses
        mocked_open.return_value = mocked_responses

        datamodels = GeonamesDataBuilder(filepath="fake_filename")
        self.assertEqual(len(datamodels), 3)

        data = datamodels[0]
        self.assertEqual(data.place_name, "Almeria")
        self.assertEqual(data.postal_code, "04001")
        self.assertEqual(data.country_code, "ES")
        self.assertEqual(data.state, "Andalucia")
        self.assertEqual(data.province, "Almeria")
        self.assertEqual(data.latitude, 36.8381)
        self.assertEqual(data.longitude, -2.4597)


if __name__ == '__main__':
    main()
