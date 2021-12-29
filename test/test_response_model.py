######################################################
#
# Author: Davide Colombo
# Date: 29/12/21 16:01
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from datetime import datetime
from unittest import TestCase, main
from airquality.response import AddFixedSensorResponse, AddMobileMeasureResponse, Channel, Geolocation


class TestResponseModel(TestCase):

    def test_raise_ValueError_when_created_geolocation(self):
        with self.assertRaises(ValueError):
            Geolocation(latitude=-92, longitude=147)

        with self.assertRaises(ValueError):
            Geolocation(latitude=97, longitude=-120)

        with self.assertRaises(ValueError):
            Geolocation(latitude=45, longitude=-190)

        with self.assertRaises(ValueError):
            Geolocation(latitude=-78, longitude=187)

    def test_create_response_for_adding_fixed_sensor(self):
        test_last_acquisition = datetime.fromtimestamp(1234567890)
        test_channels = [
            Channel(key="k1", ident="1", name="fakename1", last_acquisition=test_last_acquisition),
            Channel(key="k2", ident="2", name="fakename2", last_acquisition=test_last_acquisition),
            Channel(key="k3", ident="3", name="fakename3", last_acquisition=test_last_acquisition),
            Channel(key="k4", ident="4", name="fakename4", last_acquisition=test_last_acquisition)
        ]
        test_geolocation = Geolocation(latitude=10.99, longitude=-36.88)

        resp = AddFixedSensorResponse(
            type="faketype",
            name="fakename",
            api_param=test_channels,
            geolocation=test_geolocation
        )
        self.assertEqual(resp.type, "faketype")
        self.assertEqual(resp.name, "fakename")
        self.assertEqual(resp.api_param, test_channels)
        self.assertEqual(resp.geolocation, test_geolocation)

    def test_create_response_for_adding_mobile_sensor_measure(self):
        test_timestamp = datetime.strptime("2021-10-11T09:44:00.000Z", "%Y-%m-%dT%H:%M:%S.000Z")
        test_geolocation = Geolocation(latitude=44.98, longitude=-9.23)
        test_measures = [(1, 0.17), (2, 24), (3, 32)]

        resp = AddMobileMeasureResponse(
            timestamp=test_timestamp,
            geolocation=test_geolocation,
            measures=test_measures
        )

        self.assertEqual(resp.timestamp, test_timestamp)
        self.assertEqual(resp.geolocation, test_geolocation)
        self.assertEqual(resp.measures, test_measures)


if __name__ == '__main__':
    main()
