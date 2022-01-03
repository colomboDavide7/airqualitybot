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
from airquality.datamodel.request import AddFixedSensorsRequest, AddMobileMeasuresRequest, \
    AddSensorMeasuresRequest, Channel, AddPlacesRequest, AddWeatherForecastRequest, AddOpenWeatherMapDataRequest


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

        resp = AddFixedSensorsRequest(
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

        resp = AddMobileMeasuresRequest(
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

    ##################################### test_request_model_for_adding_geonames_country_data #####################################
    def test_request_model_for_adding_geonames_country_data(self):
        wgs84_srid = 4326
        test_geolocation = PostgisPoint(latitude=45, longitude=9, srid=wgs84_srid)

        request = AddPlacesRequest(
            placename="fakename",
            poscode="fakecode",
            state="fakestate",
            geolocation=test_geolocation,
            countrycode="fakecode",
            province="fake_province"
        )
        self.assertEqual(request.placename, "fakename")
        self.assertEqual(request.poscode, "fakecode")
        self.assertEqual(request.state, "fakestate")
        self.assertEqual(request.geolocation, test_geolocation)
        self.assertEqual(request.countrycode, "fakecode")
        self.assertEqual(request.province, "fake_province")

    ##################################### test_request_model_for_adding_geonames_country_data #####################################
    def test_request_model_for_adding_openweathermap_data(self):

        current_weather_request = AddWeatherForecastRequest(
            timestamp=datetime.fromtimestamp(1641217631+3600),
            measures=[(1, 8.84), (4, 1018), (5, 81), (6, 0.59), (7, 106)],
            weather="Clouds",
            description="overcast clouds"
        )

        hourly_forecast_request = AddWeatherForecastRequest(
            timestamp=datetime.fromtimestamp(1641214800+3600),
            measures=[(1, 9.21), (4, 1018), (5, 80), (6, 0.33), (7, 186), (8, 0.21)],
            weather="Clouds",
            description="overcast clouds"
        )

        daily_forecast_request = AddWeatherForecastRequest(
            timestamp=datetime.fromtimestamp(1641207600+3600),
            measures=[(1, 9.25), (2, 5.81), (3, 9.4), (4, 1019), (5, 83), (6, 2.72), (7, 79)],
            weather="Clouds",
            description="overcast clouds"
        )

        request = AddOpenWeatherMapDataRequest(
            current=current_weather_request,
            hourly=[hourly_forecast_request],
            daily=[daily_forecast_request]
        )

        self.assertEqual(request.current, current_weather_request)
        self.assertEqual(request.hourly[0], hourly_forecast_request)
        self.assertEqual(request.daily[0], daily_forecast_request)


if __name__ == '__main__':
    main()
