######################################################
#
# Author: Davide Colombo
# Date: 29/12/21 16:01
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from datetime import datetime
from unittest import TestCase, main
from airquality.datamodel.geometry import PostgisPoint
from airquality.datamodel.request import AddFixedSensorRequest, AddMobileMeasureRequest, AddSensorMeasuresRequest, Channel


class TestRequestModel(TestCase):

    ##################################### test_request_for_adding_fixed_sensor #####################################
    def test_request_for_adding_fixed_sensor(self):
        test_last_acquisition = datetime.fromtimestamp(1234567890)
        test_channels = [
            Channel(api_key="k1", api_id="1", channel_name="fakename1", last_acquisition=test_last_acquisition),
            Channel(api_key="k2", api_id="2", channel_name="fakename2", last_acquisition=test_last_acquisition),
            Channel(api_key="k3", api_id="3", channel_name="fakename3", last_acquisition=test_last_acquisition),
            Channel(api_key="k4", api_id="4", channel_name="fakename4", last_acquisition=test_last_acquisition)
        ]
        test_geolocation = PostgisPoint(latitude=10.99, longitude=-36.88)

        resp = AddFixedSensorRequest(
            type="faketype",
            name="fakename",
            channels=test_channels,
            geolocation=test_geolocation
        )
        self.assertEqual(resp.type, "faketype")
        self.assertEqual(resp.name, "fakename")
        self.assertEqual(resp.channels, test_channels)
        self.assertEqual(resp.geolocation, test_geolocation)

    ##################################### test_request_for_adding_mobile_sensor_measure #####################################
    def test_request_for_adding_mobile_sensor_measure(self):
        test_timestamp = datetime.strptime("2021-10-11T09:44:00.000Z", "%Y-%m-%dT%H:%M:%S.000Z")
        test_geolocation = PostgisPoint(latitude=44.98, longitude=-9.23)
        test_measures = [(1, 0.17), (2, 24), (3, 32)]

        resp = AddMobileMeasureRequest(
            timestamp=test_timestamp, geolocation=test_geolocation, measures=test_measures
        )
        self.assertEqual(resp.timestamp, test_timestamp)
        self.assertEqual(resp.geolocation, test_geolocation)
        self.assertEqual(resp.measures, test_measures)

    ##################################### test_request_for_adding_mobile_sensor_measure #####################################
    def test_request_for_adding_station_measures(self):
        test_timestamp = datetime.strptime("2021-12-20T11:18:40Z", "%Y-%m-%dT%H:%M:%SZ")
        test_mesures = [(12, 20.50), (13, 35.53), (14, 37.43), (15, 55), (16, 60)]

        request = AddSensorMeasuresRequest(timestamp=test_timestamp, measures=test_mesures)
        self.assertEqual(request.timestamp, test_timestamp)
        self.assertEqual(request.measures, test_mesures)


if __name__ == '__main__':
    main()
