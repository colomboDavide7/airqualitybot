######################################################
#
# Author: Davide Colombo
# Date: 29/12/21 16:00
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from datetime import datetime
from unittest import TestCase, main
from airquality.request import AddPurpleairSensorRequest, AddAtmotubeMeasureRequest
from airquality.response import Geolocation, Channel
from airquality.response_builder import AddPurpleairSensorResponseBuilder, AddAtmotubeMeasureResponseBuilder


class TestResponseBuilder(TestCase):

    def test_create_response_for_adding_purpleair_sensor(self):
        test_request_model = AddPurpleairSensorRequest(
            name="fakename",
            sensor_index=9,
            latitude=1.234,
            longitude=5.666,
            altitude=0,
            primary_id_a=111,
            primary_key_a="key1a",
            primary_id_b=222,
            primary_key_b="key1b",
            secondary_id_a=333,
            secondary_key_a="key2a",
            secondary_id_b=444,
            secondary_key_b="key2b",
            date_created=1234567890
        )

        resp = AddPurpleairSensorResponseBuilder(request=test_request_model).build_response()

        expected_last_acquisition = datetime.fromtimestamp(1234567890)
        expected_api_param = [
            Channel(api_key="key1a", api_id="111", channel_name="1A", last_acquisition=expected_last_acquisition),
            Channel(api_key="key1b", api_id="222", channel_name="1B", last_acquisition=expected_last_acquisition),
            Channel(api_key="key2a", api_id="333", channel_name="2A", last_acquisition=expected_last_acquisition),
            Channel(api_key="key2b", api_id="444", channel_name="2B", last_acquisition=expected_last_acquisition)
        ]
        expected_geolocation = Geolocation(latitude=1.234, longitude=5.666)

        self.assertEqual(resp.type, "Purpleair/Thingspeak")
        self.assertEqual(resp.name, "fakename (9)")
        self.assertEqual(resp.channels, expected_api_param)
        self.assertEqual(resp.geolocation, expected_geolocation)

    def test_create_response_for_adding_atmotube_measure(self):
        test_code2id = {'voc': 66, 'pm1': 48, 'pm25': 94, 'pm10': 2, 't': 4, 'h': 12, 'p': 39}

        test_request_model = AddAtmotubeMeasureRequest(
            time="2021-08-10T23:59:00.000Z",
            voc=0.17,
            pm1=8,
            pm25=10,
            pm10=11,
            temperature=29,
            humidity=42,
            pressure=1004.68,
            latitude=45.765,
            longitude=9.897
        )

        resp = AddAtmotubeMeasureResponseBuilder(request=test_request_model, code2id=test_code2id).build_response()

        expected_timestamp = datetime.strptime("2021-08-10T23:59:00.000Z", "%Y-%m-%dT%H:%M:%S.000Z")
        expected_geolocation = Geolocation(latitude=45.765, longitude=9.897)
        expected_measures = [(66, 0.17), (48, 8), (94, 10), (2, 11), (4, 29), (12, 42), (39, 1004.68)]

        self.assertEqual(resp.timestamp, expected_timestamp)
        self.assertEqual(resp.geolocation, expected_geolocation)
        self.assertEqual(resp.measures, expected_measures)


if __name__ == '__main__':
    main()
