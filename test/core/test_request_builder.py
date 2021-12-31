######################################################
#
# Author: Davide Colombo
# Date: 29/12/21 16:00
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from datetime import datetime
from unittest import TestCase, main
from unittest.mock import MagicMock
from airquality.datamodel.request import Channel
from airquality.datamodel.geometry import NullGeometry, PostgisPoint
from airquality.datamodel.apidata import PurpleairAPIData, AtmotubeAPIData
from airquality.core.request_builder import AddPurpleairSensorRequestBuilder, AddAtmotubeMeasureRequestBuilder


class TestRequestBuilder(TestCase):

    @property
    def get_test_purpleair_datamodel(self):
        return PurpleairAPIData(
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

    ##################################### test_create_request_for_adding_purpleair_sensor #####################################
    def test_create_request_for_adding_purpleair_sensor(self):
        mocked_datamodel_builder = MagicMock()
        mocked_datamodel_builder.__iter__.return_value = [self.get_test_purpleair_datamodel]

        requests = AddPurpleairSensorRequestBuilder(datamodel=mocked_datamodel_builder)
        self.assertEqual(len(requests), 1)
        req1 = requests[0]

        expected_last_acquisition = datetime.fromtimestamp(1234567890)
        expected_api_param = [
            Channel(api_key="key1a", api_id="111", channel_name="1A", last_acquisition=expected_last_acquisition),
            Channel(api_key="key1b", api_id="222", channel_name="1B", last_acquisition=expected_last_acquisition),
            Channel(api_key="key2a", api_id="333", channel_name="2A", last_acquisition=expected_last_acquisition),
            Channel(api_key="key2b", api_id="444", channel_name="2B", last_acquisition=expected_last_acquisition)
        ]
        expected_geolocation = PostgisPoint(latitude=1.234, longitude=5.666)

        self.assertEqual(req1.type, "Purpleair/Thingspeak")
        self.assertEqual(req1.name, "fakename (9)")
        self.assertEqual(req1.channels, expected_api_param)
        self.assertEqual(req1.geolocation, expected_geolocation)

    @property
    def get_test_atmotube_datamodel(self):
        return AtmotubeAPIData(
            time="2021-08-10T23:59:00.000Z",
            voc=0.17,
            pm1=8,
            pm25=10,
            pm10=11,
            t=29,
            h=42,
            p=1004.68,
            coords={'lat': 45.765, 'lon': 9.897}
        )

    @property
    def get_test_atmotube_datamodel_without_coords(self):
        return AtmotubeAPIData(
            time="2021-08-11T00:00:00.000Z",
            voc=0.19,
            pm1=7,
            p=1007.03
        )

    ##################################### test_create_request_for_adding_atmotube_measure #####################################
    def test_create_request_for_adding_atmotube_measure(self):
        test_code2id = {'voc': 66, 'pm1': 48, 'pm25': 94, 'pm10': 2, 't': 4, 'h': 12, 'p': 39}
        mocked_datamodel_builder = MagicMock()
        mocked_datamodel_builder.__iter__.return_value = [self.get_test_atmotube_datamodel, self.get_test_atmotube_datamodel_without_coords]

        requests = AddAtmotubeMeasureRequestBuilder(datamodel=mocked_datamodel_builder, code2id=test_code2id)
        self.assertEqual(len(requests), 2)
        req1 = requests[0]

        expected_timestamp = datetime.strptime("2021-08-10T23:59:00.000Z", "%Y-%m-%dT%H:%M:%S.000Z")
        expected_geolocation = PostgisPoint(latitude=45.765, longitude=9.897)
        expected_measures = [(66, 0.17), (48, 8), (94, 10), (2, 11), (4, 29), (12, 42), (39, 1004.68)]

        self.assertEqual(req1.timestamp, expected_timestamp)
        self.assertEqual(req1.geolocation, expected_geolocation)
        self.assertEqual(req1.measures, expected_measures)

        req2 = requests[1]
        expected_timestamp = datetime.strptime("2021-08-11T00:00:00.000Z", "%Y-%m-%dT%H:%M:%S.000Z")
        expected_measures = [(66, 0.19), (48, 7), (39, 1007.03)]
        self.assertEqual(req2.timestamp, expected_timestamp)
        self.assertEqual(req2.measures, expected_measures)
        self.assertIsInstance(req2.geolocation, NullGeometry)


if __name__ == '__main__':
    main()
