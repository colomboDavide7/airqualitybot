######################################################
#
# Author: Davide Colombo
# Date: 29/12/21 16:01
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from datetime import datetime
from unittest import TestCase, main
from airquality.request import AddFixedSensorRequest, AddMobileMeasureRequest, Channel, Geolocation, NullGeolocation


class TestRequestModel(TestCase):

    def test_geometry_from_geolocation(self):
        geo = Geolocation(latitude=5, longitude=10)
        self.assertEqual(geo.geometry, "POINT(10 5)")
        self.assertEqual(geo.geometry_as_text, "ST_GeomFromText('POINT(10 5)', 26918)")

    def test_null_geolocation(self):
        geo = NullGeolocation()
        self.assertEqual(geo.geometry, "NULL")
        self.assertEqual(geo.geometry_as_text, "NULL")

    def test_raise_ValueError_when_create_geolocation(self):
        with self.assertRaises(ValueError):
            Geolocation(latitude=-92, longitude=147)

        with self.assertRaises(ValueError):
            Geolocation(latitude=97, longitude=-120)

        with self.assertRaises(ValueError):
            Geolocation(latitude=45, longitude=-190)

        with self.assertRaises(ValueError):
            Geolocation(latitude=-78, longitude=187)

    def test_request_for_adding_fixed_sensor(self):
        test_last_acquisition = datetime.fromtimestamp(1234567890)
        test_channels = [
            Channel(api_key="k1", api_id="1", channel_name="fakename1", last_acquisition=test_last_acquisition),
            Channel(api_key="k2", api_id="2", channel_name="fakename2", last_acquisition=test_last_acquisition),
            Channel(api_key="k3", api_id="3", channel_name="fakename3", last_acquisition=test_last_acquisition),
            Channel(api_key="k4", api_id="4", channel_name="fakename4", last_acquisition=test_last_acquisition)
        ]
        test_geolocation = Geolocation(latitude=10.99, longitude=-36.88)

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

    def test_request_for_adding_mobile_sensor_measure(self):
        test_timestamp = datetime.strptime("2021-10-11T09:44:00.000Z", "%Y-%m-%dT%H:%M:%S.000Z")
        test_geolocation = Geolocation(latitude=44.98, longitude=-9.23)
        test_measures = [(1, 0.17), (2, 24), (3, 32)]

        resp = AddMobileMeasureRequest(
            timestamp=test_timestamp,
            geolocation=test_geolocation,
            measures=test_measures
        )

        self.assertEqual(resp.timestamp, test_timestamp)
        self.assertEqual(resp.geolocation, test_geolocation)
        self.assertEqual(resp.measures, test_measures)


if __name__ == '__main__':
    main()
