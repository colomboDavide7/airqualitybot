######################################################
#
# Author: Davide Colombo
# Date: 29/12/21 18:18
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from datetime import datetime
import test._test_utils as tutils
from unittest import TestCase, main
from unittest.mock import MagicMock
from airquality.iterables.responses import WeatherDataIterableResponses
from airquality.datamodel.requests import WeatherConditionsRequest, AddWeatherDataRequest, WeatherAlertRequest


def _rome_timezone():
    return tutils.get_tzinfo_from_timezone_name(tzname='Europe/Rome')


def _current_weather_request():
    return WeatherConditionsRequest(
        timestamp=datetime.utcfromtimestamp(1641217631 + 3600),
        sunrise=datetime.utcfromtimestamp(1641193337),
        sunset=datetime.utcfromtimestamp(1641225175),
        temperature=8.84,
        pressure=1018,
        humidity=81,
        wind_speed=0.59,
        wind_direction=106,
        weather_id=55
    )


def _hourly_forecast_request():
    return WeatherConditionsRequest(
        timestamp=datetime.utcfromtimestamp(1641214800 + 3600),
        temperature=9.21,
        pressure=1018,
        humidity=80,
        wind_speed=0.33,
        wind_direction=186,
        rain=0.21,
        pop=0,
        weather_id=55
    )


def _daily_forecast_request():
    return WeatherConditionsRequest(
        timestamp=datetime.utcfromtimestamp(1641207600 + 3600),
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


def _weather_alert_request():
    return WeatherAlertRequest(
        sender_name='Fake sender',
        alert_event='Fake event',
        alert_begin=datetime(2022, 1, 24, 19, tzinfo=_rome_timezone()),
        alert_until=datetime(2022, 1, 25, 9, 59, tzinfo=_rome_timezone()),
        description='Fake description'
    )


def _openweathermap_request():
    return AddWeatherDataRequest(
        current=_current_weather_request(),
        hourly=[_hourly_forecast_request()],
        daily=[_daily_forecast_request()],
        alerts=[_weather_alert_request()]
    )


def _mocked_request_builder():
    mocked_rb = MagicMock()
    mocked_rb.__len__.return_value = 1
    mocked_rb.__iter__.return_value = [_openweathermap_request()]
    return mocked_rb


def _expected_current_weather_record():
    return "(14400,55,8.84,1018,81,0.59,106,NULL,NULL," \
           "'2022-01-03 14:47:11','2022-01-03 07:02:17','2022-01-03 15:52:55')"


def _expected_hourly_forecast_record():
    return "(14400,55,9.21,1018,80,0.33,186,0.21,0,NULL,'2022-01-03 14:00:00')"


def _expected_daily_forecast_record():
    return "(14400,55,9.25,5.81,9.4,1019,83,2.72,79,NULL,0.01,NULL,'2022-01-03 12:00:00')"


def _expected_weather_alert_record():
    return "(14400,'Fake sender','Fake event'," \
           "'2022-01-24 19:00:00+01:00','2022-01-25 09:59:00+01:00'," \
           "'Fake description')"


class TestAddOpenweathermapDataResponseBuilder(TestCase):

# =========== SETUP METHOD
    def setUp(self) -> None:
        self._response_builder = WeatherDataIterableResponses(
            requests=_mocked_request_builder(),
            geoarea_id=14400
        )

# =========== TEST METHOD
    def test_create_response_to_request_of_adding_openweathermap_data(self):
        self.assertEqual(
            len(self._response_builder),
            1
        )
        self._assert_response()

# =========== SUPPORT METHOD
    def _assert_response(self):
        resp = self._response_builder[0]
        self.assertEqual(
            resp.current_weather_record,
            _expected_current_weather_record()
        )
        self.assertEqual(
            resp.hourly_forecast_record,
            _expected_hourly_forecast_record()
        )
        self.assertEqual(
            resp.daily_forecast_record,
            _expected_daily_forecast_record()
        )
        self.assertEqual(
            resp.weather_alert_record,
            _expected_weather_alert_record()
        )


if __name__ == '__main__':
    main()
