######################################################
#
# Author: Davide Colombo
# Date: 29/12/21 16:01
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from datetime import datetime
from unittest import TestCase, main
from airquality.datamodel.request import AddWeatherForecastRequest, AddOpenWeatherMapDataRequest


def _current_weather_test_request():
    return AddWeatherForecastRequest(
        timestamp=datetime.utcfromtimestamp(1641217631+3600),
        sunrise=datetime.utcfromtimestamp(1641193337),
        sunset=datetime.utcfromtimestamp(1641225175),
        temperature=8.84,
        pressure=1018,
        humidity=81,
        wind_speed=0.59,
        wind_direction=106,
        weather_id=55
    )


def _hourly_forecast_test_request():
    return AddWeatherForecastRequest(
        timestamp=datetime.utcfromtimestamp(1641214800+3600),
        temperature=9.21,
        pressure=1018,
        humidity=80,
        wind_speed=0.33,
        wind_direction=186,
        rain=0.21,
        pop=0,
        weather_id=55
    )


def _daily_forecast_test_request():
    return AddWeatherForecastRequest(
        timestamp=datetime.utcfromtimestamp(1641207600+3600),
        temperature=9.25,
        min_temp=5.81,
        max_temp=9.4,
        pressure=1019,
        humidity=83,
        wind_speed=2.72,
        wind_direction=79,
        weather_id=55,
        pop=0.01
    )


class TestAddOpenweathermapDataRequest(TestCase):

# =========== TEST METHODS
    def test_add_openweathermap_data_request(self):
        request = AddOpenWeatherMapDataRequest(
            current=_current_weather_test_request(),
            hourly=[_hourly_forecast_test_request()],
            daily=[_daily_forecast_test_request()]
        )
        self._assert_current_weather(request.current)
        self._assert_hourly_forecast(request.hourly[0])
        self._assert_daily_forecast(request.daily[0])

# =========== SUPPORT METHODS
    def _assert_current_weather(self, request: AddWeatherForecastRequest):
        self.assertEqual(request.timestamp, datetime(2022, 1, 3, 14, 47, 11))
        self.assertEqual(request.sunrise, datetime(2022, 1, 3, 7, 2, 17))
        self.assertEqual(request.sunset, datetime(2022, 1, 3, 15, 52, 55))
        self.assertEqual(request.temperature, 8.84)
        self.assertEqual(request.pressure, 1018)
        self.assertEqual(request.humidity, 81)
        self.assertEqual(request.wind_speed, 0.59)
        self.assertEqual(request.wind_direction, 106)
        self.assertEqual(request.weather_id, 55)
        self.assertIsNone(request.rain)
        self.assertIsNone(request.snow)
        self.assertIsNone(request.min_temp)
        self.assertIsNone(request.max_temp)
        self.assertIsNone(request.pop)

    def _assert_hourly_forecast(self, request: AddWeatherForecastRequest):
        self.assertEqual(request.timestamp, datetime(2022, 1, 3, 14))
        self.assertEqual(request.temperature, 9.21)
        self.assertEqual(request.pressure, 1018)
        self.assertEqual(request.humidity, 80)
        self.assertEqual(request.wind_speed, 0.33)
        self.assertEqual(request.wind_direction, 186)
        self.assertEqual(request.weather_id, 55)
        self.assertEqual(request.rain, 0.21)
        self.assertEqual(request.pop, 0)
        self.assertIsNone(request.snow)
        self.assertIsNone(request.min_temp)
        self.assertIsNone(request.max_temp)
        self.assertIsNone(request.sunset)
        self.assertIsNone(request.sunrise)

    def _assert_daily_forecast(self, request: AddWeatherForecastRequest):
        self.assertEqual(request.timestamp, datetime(2022, 1, 3, 12))
        self.assertEqual(request.temperature, 9.25)
        self.assertEqual(request.min_temp, 5.81)
        self.assertEqual(request.max_temp, 9.4)
        self.assertEqual(request.pressure, 1019)
        self.assertEqual(request.humidity, 83)
        self.assertEqual(request.wind_speed, 2.72)
        self.assertEqual(request.wind_direction, 79)
        self.assertEqual(request.weather_id, 55)
        self.assertEqual(request.pop, 0.01)
        self.assertIsNone(request.rain)
        self.assertIsNone(request.snow)
        self.assertIsNone(request.sunset)
        self.assertIsNone(request.sunrise)


if __name__ == '__main__':
    main()
