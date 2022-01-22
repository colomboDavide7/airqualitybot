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
from airquality.datamodel.geometry import PostgisPoint
from airquality.datamodel.apidata import GeonamesData, Weather, WeatherForecast, \
    OpenWeatherMapAPIData
from airquality.core.request_builder import AddPlacesRequestBuilder, AddOpenWeatherMapDataRequestBuilder


class TestRequestBuilder(TestCase):

    @property
    def get_test_geonames_data(self):
        line = ["IT", "27100", "Pavia'", "Lombardia'", "statecode", "Pavia'", "PV", "community", "communitycode", "45", "9", "4"]
        return GeonamesData(*line)

    ############################## test_create_requests_for_adding_places #############################
    def test_create_requests_for_adding_places(self):
        mocked_datamodel_builder = MagicMock()
        mocked_datamodel_builder.__len__.return_value = 1
        mocked_datamodel_builder.__iter__.return_value = [self.get_test_geonames_data]

        requests = AddPlacesRequestBuilder(datamodels=mocked_datamodel_builder)
        self.assertEqual(len(requests), 1)
        req = requests[0]

        expected_geolocation = PostgisPoint(latitude=45, longitude=9, srid=4326)
        self.assertEqual(req.poscode, "27100")
        self.assertEqual(req.geolocation, expected_geolocation)
        self.assertEqual(req.placename, "Pavia")
        self.assertEqual(req.state, "Lombardia")
        self.assertEqual(req.province, "Pavia")
        self.assertEqual(req.countrycode, "IT")

    @property
    def get_test_current_weather_data(self):
        return WeatherForecast(
            dt=1641217631+3600,
            temp=8.84,
            pressure=1018,
            humidity=81,
            wind_speed=0.59,
            wind_deg=106,
            weather=[Weather(id=804, icon="04d", main="Clouds", description="overcast clouds")]
        )

    @property
    def get_test_hourly_forecast_data(self):
        return WeatherForecast(
            dt=1641214800+3600,
            temp=9.21,
            pressure=1018,
            humidity=80,
            wind_speed=0.33,
            wind_deg=186,
            weather=[Weather(id=804, icon="04d", main="Clouds", description="overcast clouds")],
            rain=0.21
        )

    @property
    def get_test_daily_forecast_data(self):
        return WeatherForecast(
            dt=1641207600+3600,
            temp=9.25,
            temp_min=5.81,
            temp_max=9.4,
            pressure=1019,
            humidity=83,
            wind_speed=2.72,
            wind_deg=79,
            weather=[Weather(id=804, icon="04d", main="Clouds", description="overcast clouds")]
        )

    @property
    def get_test_openweathermap_apidata(self):
        return OpenWeatherMapAPIData(
            current=self.get_test_current_weather_data,
            hourly_forecast=[self.get_test_hourly_forecast_data],
            daily_forecast=[self.get_test_daily_forecast_data]
        )

    ############################## test_create_request_for_adding_openweathermap_data #############################
    def test_create_request_for_adding_openweathermap_data(self):
        mocked_datamodel_builder = MagicMock()
        mocked_datamodel_builder.__len__.return_value = 1
        mocked_datamodel_builder.__iter__.return_value = [self.get_test_openweathermap_apidata]

        test_weather_map = {804: {'04d': 55, '04n': 56}, 500: {"13d": 37}}

        requests = AddOpenWeatherMapDataRequestBuilder(
            datamodels=mocked_datamodel_builder, weather_map=test_weather_map
        )
        self.assertEqual(len(requests), 1)

        req = requests[0]
        self.assertEqual(req.current.timestamp, datetime.utcfromtimestamp(1641217631+3600))
        self.assertEqual(req.current.weather_id, 55)
        self.assertEqual(req.current.temperature, 8.84)
        self.assertEqual(req.current.pressure, 1018)
        self.assertEqual(req.current.humidity, 81)
        self.assertEqual(req.current.wind_speed, 0.59)
        self.assertEqual(req.current.wind_direction, 106)
        self.assertIsNone(req.current.rain)
        self.assertIsNone(req.current.snow)
        self.assertIsNone(req.current.min_temp)
        self.assertIsNone(req.current.max_temp)

        hourly1 = req.hourly[0]
        self.assertEqual(hourly1.timestamp, datetime.utcfromtimestamp(1641214800+3600))
        self.assertEqual(hourly1.weather_id, 55)
        self.assertEqual(hourly1.temperature, 9.21)
        self.assertEqual(hourly1.pressure, 1018)
        self.assertEqual(hourly1.humidity, 80)
        self.assertEqual(hourly1.wind_speed, 0.33)
        self.assertEqual(hourly1.wind_direction, 186)
        self.assertEqual(hourly1.rain, 0.21)
        self.assertIsNone(hourly1.snow)
        self.assertIsNone(hourly1.min_temp)
        self.assertIsNone(hourly1.max_temp)

        daily1 = req.daily[0]
        self.assertEqual(daily1.timestamp, datetime.utcfromtimestamp(1641207600+3600))
        self.assertEqual(daily1.weather_id, 55)
        self.assertEqual(daily1.temperature, 9.25)
        self.assertEqual(daily1.pressure, 1019)
        self.assertEqual(daily1.humidity, 83)
        self.assertEqual(daily1.wind_speed, 2.72)
        self.assertEqual(daily1.wind_direction, 79)
        self.assertIsNone(daily1.rain)
        self.assertIsNone(daily1.snow)
        self.assertEqual(daily1.min_temp, 5.81)
        self.assertEqual(daily1.max_temp, 9.4)


if __name__ == '__main__':
    main()
