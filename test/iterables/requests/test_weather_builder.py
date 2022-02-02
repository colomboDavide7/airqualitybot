######################################################
#
# Author: Davide Colombo
# Date: 29/12/21 16:00
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from datetime import datetime
import test._test_utils as tutils
from unittest import TestCase, main
from unittest.mock import MagicMock
from airquality.extra.timest import Timest
from airquality.datamodel.fromapi import WeatherDM, WeatherConditionsDM, OpenweathermapDM, WeatherAlertDM
from airquality.iterables.requests import AddOpenWeatherMapDataRequestBuilder


def _test_timezone_name():
    return "America/New_York"


def _test_weather():
    return WeatherDM(
        id=804,
        icon="04d",
        main="Clouds",
        description="overcast clouds"
    )


def _test_current_weather_data():
    return WeatherConditionsDM(
        dt=1641217631,
        sunset=1641225175,
        sunrise=1641193337,
        temp=8.84,
        pressure=1018,
        humidity=81,
        wind_speed=0.59,
        wind_deg=106,
        weather=[_test_weather()]
    )


def _test_hourly_forecast_data():
    return WeatherConditionsDM(
        dt=1641214800,
        temp=9.21,
        pressure=1018,
        humidity=80,
        wind_speed=0.33,
        wind_deg=186,
        weather=[_test_weather()],
        rain=0.21,
        pop=0
    )


def _test_daily_forecast_data():
    return WeatherConditionsDM(
        dt=1641207600,
        temp=9.25,
        temp_min=5.81,
        temp_max=9.4,
        pressure=1019,
        humidity=83,
        wind_speed=2.72,
        wind_deg=79,
        weather=[_test_weather()],
        pop=0.01
    )


def _test_weather_alert():
    return WeatherAlertDM(
        sender_name='fake sender',
        alert_event='fake event',
        alert_begin=1643047200,
        alert_until=1643101140,
        description='fake description'
    )


def _test_openweathermap_datamodel():
    return OpenweathermapDM(
        tz_name=_test_timezone_name(),
        current=_test_current_weather_data(),
        hourly_forecast=[_test_hourly_forecast_data()],
        daily_forecast=[_test_daily_forecast_data()],
        alerts=[_test_weather_alert()]
    )


def _test_weather_conditions_mapping():
    return {804: {'04d': 55, '04n': 56}, 500: {"13d": 37}}


def _mocked_datamodel_builder():
    mocked_db = MagicMock()
    mocked_db.__len__.return_value = 1
    mocked_db.__iter__.return_value = [_test_openweathermap_datamodel()]
    return mocked_db


def _expected_timezone_info():
    return tutils.get_tzinfo_from_timezone_name(_test_timezone_name())


class TestAddWeatherDataRequestBuilder(TestCase):

# =========== SETUP METHOD
    def setUp(self) -> None:
        self._builder = AddOpenWeatherMapDataRequestBuilder(
            datamodels=_mocked_datamodel_builder(),
            weather_map=_test_weather_conditions_mapping(),
            timest=Timest()
        )

# =========== TEST METHOD
    def test_create_request_for_adding_openweathermap_data(self):
        self.assertEqual(
            len(self._builder),
            1
        )
        self._assert_current_weather()
        self._assert_hourly_forecast()
        self._assert_daily_forecast()

# =========== SUPPORT METHODS
    def _assert_weather_alerts(self):
        alerts = self._builder[0].alerts
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0].sender_name, 'fake sender')
        self.assertEqual(alerts[0].alert_event, 'fake event')
        self.assertEqual(
            alerts[0].alert_begin,
            datetime(2022, 1, 24, 13, tzinfo=_expected_timezone_info())
        )
        self.assertEqual(
            alerts[0].alert_until,
            datetime(2022, 1, 25, 3, 59, tzinfo=_expected_timezone_info())
        )
        self.assertEqual(alerts[0].description, 'fake description')

    def _assert_current_weather(self):
        req = self._builder[0]
        self.assertEqual(
            req.current.timestamp,
            datetime(2022, 1, 3, 8, 47, 11, tzinfo=_expected_timezone_info())
        )
        self.assertEqual(
            req.current.sunrise,
            datetime(2022, 1, 3, 2, 2, 17, tzinfo=_expected_timezone_info())
        )
        self.assertEqual(
            req.current.sunset,
            datetime(2022, 1, 3, 10, 52, 55, tzinfo=_expected_timezone_info())
        )
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
        self.assertIsNone(req.current.pop)

    def _assert_hourly_forecast(self):
        hourly = self._builder[0].hourly[0]
        self.assertEqual(
            hourly.timestamp,
            datetime(2022, 1, 3, 8, tzinfo=_expected_timezone_info())
        )
        self.assertEqual(hourly.weather_id, 55)
        self.assertEqual(hourly.temperature, 9.21)
        self.assertEqual(hourly.pressure, 1018)
        self.assertEqual(hourly.humidity, 80)
        self.assertEqual(hourly.wind_speed, 0.33)
        self.assertEqual(hourly.wind_direction, 186)
        self.assertEqual(hourly.rain, 0.21)
        self.assertEqual(hourly.pop, 0)
        self.assertIsNone(hourly.snow)
        self.assertIsNone(hourly.min_temp)
        self.assertIsNone(hourly.max_temp)
        self.assertIsNone(hourly.sunrise)
        self.assertIsNone(hourly.sunset)

    def _assert_daily_forecast(self):
        daily = self._builder[0].daily[0]
        self.assertEqual(
            daily.timestamp,
            datetime(2022, 1, 3, 6, tzinfo=_expected_timezone_info())
        )
        self.assertEqual(daily.weather_id, 55)
        self.assertEqual(daily.temperature, 9.25)
        self.assertEqual(daily.pressure, 1019)
        self.assertEqual(daily.humidity, 83)
        self.assertEqual(daily.wind_speed, 2.72)
        self.assertEqual(daily.wind_direction, 79)
        self.assertEqual(daily.pop, 0.01)
        self.assertIsNone(daily.rain)
        self.assertIsNone(daily.snow)
        self.assertEqual(daily.min_temp, 5.81)
        self.assertEqual(daily.max_temp, 9.4)
        self.assertIsNone(daily.sunrise)
        self.assertIsNone(daily.sunset)


if __name__ == '__main__':
    main()
