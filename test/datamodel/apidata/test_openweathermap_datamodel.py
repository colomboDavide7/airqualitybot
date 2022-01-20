######################################################
#
# Author: Davide Colombo
# Date: 29/12/21 15:43
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from unittest import TestCase, main
from airquality.datamodel.apidata import Weather, WeatherForecast, OpenWeatherMapAPIData, WeatherCityData


def _weather_test_data():
    return Weather(
            id=804,
            icon="04d",
            main="Clouds",
            description="overcast clouds"
        )


def _current_weather_test_datamodel():
    return WeatherForecast(
            dt=1641217631,
            temp=8.84,
            pressure=1018,
            humidity=81,
            wind_speed=0.59,
            wind_deg=106,
            weather=[_weather_test_data()]
        )


def _hourly_forecast_test_datamodel():
    return WeatherForecast(
            dt=1641214800,
            temp=9.21,
            pressure=1018,
            humidity=80,
            wind_speed=0.33,
            wind_deg=186,
            weather=[_weather_test_data()]
        )


def _daily_forecast_test_datamodel():
    return WeatherForecast(
            dt=1641207600,
            temp=9.25,
            temp_min=5.81,
            temp_max=9.4,
            pressure=1019,
            humidity=83,
            wind_speed=2.72,
            wind_deg=79,
            weather=[_weather_test_data()]
        )


class TestOpenWeatherMapDatamodel(TestCase):
    """
    A class that tests the openweathermap datamodels.
    """

# =========== TEST METHODS
    def test_weathercity_datamodel(self):
        data = WeatherCityData(
            country_code="fakecode",
            place_name="fakename"
        )
        self.assertEqual(data.country_code, "fakecode")
        self.assertEqual(data.place_name, "fakename")
        self.assertEqual(repr(data), "WeatherCityData(country_code=fakecode, place_name=fakename)")

    def test_weather_data(self):
        self._assert_weather(_weather_test_data())

    def test_onecallapi_current_weather_datamodel(self):
        current_weather = _current_weather_test_datamodel()
        self._assert_current_weather(current_weather)
        self._assert_weather(current_weather.weather[0])

    def test_onecallapi_hourly_forecast_datamodel(self):
        hourly_forecast = _hourly_forecast_test_datamodel()
        self._assert_hourly_forecast(hourly_forecast)
        self._assert_weather(hourly_forecast.weather[0])

    def test_onecallapi_daily_forecast_datamodel(self):
        daily_forecast = _daily_forecast_test_datamodel()
        self._assert_daily_forecast(daily_forecast)
        self._assert_weather(daily_forecast.weather[0])

    def test_full_openweathermap_datamodel(self):
        data = OpenWeatherMapAPIData(
            current=_current_weather_test_datamodel(),
            hourly_forecast=[_hourly_forecast_test_datamodel()],
            daily_forecast=[_daily_forecast_test_datamodel()]
        )
        self._assert_current_weather(data.current)
        self._assert_hourly_forecast(data.hourly_forecast[0])
        self._assert_daily_forecast(data.daily_forecast[0])

# =========== SUPPORT METHODS
    def _assert_weather(self, weather_data):
        self.assertEqual(weather_data.id, 804)
        self.assertEqual(weather_data.icon, "04d")
        self.assertEqual(weather_data.main, "Clouds")
        self.assertEqual(weather_data.description, "overcast clouds")

    def _assert_current_weather(self, current_weather: WeatherForecast):
        self.assertEqual(current_weather.dt, 1641217631)
        self.assertEqual(current_weather.temp, 8.84)
        self.assertEqual(current_weather.pressure, 1018)
        self.assertEqual(current_weather.humidity, 81)
        self.assertEqual(current_weather.wind_speed, 0.59)
        self.assertEqual(current_weather.wind_deg, 106)
        self.assertEqual(len(current_weather.weather), 1)
        self.assertIsNone(current_weather.temp_max)
        self.assertIsNone(current_weather.temp_min)
        self.assertIsNone(current_weather.rain)
        self.assertIsNone(current_weather.snow)

    def _assert_hourly_forecast(self, hourly_forecast: WeatherForecast):
        self.assertEqual(hourly_forecast.dt, 1641214800)
        self.assertEqual(hourly_forecast.temp, 9.21)
        self.assertEqual(hourly_forecast.pressure, 1018)
        self.assertEqual(hourly_forecast.humidity, 80)
        self.assertEqual(hourly_forecast.wind_speed, 0.33)
        self.assertEqual(hourly_forecast.wind_deg, 186)
        self.assertEqual(len(hourly_forecast.weather), 1)
        self.assertIsNone(hourly_forecast.temp_max)
        self.assertIsNone(hourly_forecast.temp_min)
        self.assertIsNone(hourly_forecast.rain)
        self.assertIsNone(hourly_forecast.snow)

    def _assert_daily_forecast(self, daily_forecast: WeatherForecast):
        self.assertEqual(daily_forecast.dt, 1641207600)
        self.assertEqual(daily_forecast.temp, 9.25)
        self.assertEqual(daily_forecast.temp_min, 5.81)
        self.assertEqual(daily_forecast.temp_max, 9.4)
        self.assertEqual(daily_forecast.pressure, 1019)
        self.assertEqual(daily_forecast.humidity, 83)
        self.assertEqual(daily_forecast.wind_speed, 2.72)
        self.assertEqual(daily_forecast.wind_deg, 79)
        self.assertEqual(len(daily_forecast.weather), 1)
        self.assertIsNone(daily_forecast.rain)
        self.assertIsNone(daily_forecast.snow)


if __name__ == '__main__':
    main()
