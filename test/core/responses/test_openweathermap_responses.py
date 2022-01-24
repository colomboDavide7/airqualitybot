######################################################
#
# Author: Davide Colombo
# Date: 29/12/21 18:18
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from datetime import datetime
from unittest import TestCase, main
from unittest.mock import MagicMock
from airquality.core.response_builder import AddOpenWeatherMapDataResponseBuilder
from airquality.datamodel.request import AddWeatherForecastRequest, AddOpenWeatherMapDataRequest


def _current_weather_request():
    return AddWeatherForecastRequest(
        timestamp=datetime.utcfromtimestamp(1641217631 + 3600),
        temperature=8.84,
        pressure=1018,
        humidity=81,
        wind_speed=0.59,
        wind_direction=106,
        weather_id=55
    )


def _hourly_forecast_request():
    return AddWeatherForecastRequest(
        timestamp=datetime.utcfromtimestamp(1641214800 + 3600),
        temperature=9.21,
        pressure=1018,
        humidity=80,
        wind_speed=0.33,
        wind_direction=186,
        rain=0.21,
        weather_id=55
    )


def _daily_forecast_request():
    return AddWeatherForecastRequest(
        timestamp=datetime.utcfromtimestamp(1641207600 + 3600),
        temperature=9.25,
        min_temp=5.81,
        max_temp=9.4,
        pressure=1019,
        humidity=83,
        wind_speed=2.72,
        wind_direction=79,
        weather_id=55
    )


def _openweathermap_request():
    return AddOpenWeatherMapDataRequest(
        current=_current_weather_request(),
        hourly=[_hourly_forecast_request()],
        daily=[_daily_forecast_request()]
    )


def _mocked_request_builder():
    mocked_rb = MagicMock()
    mocked_rb.__len__.return_value = 1
    mocked_rb.__iter__.return_value = [_openweathermap_request()]
    return mocked_rb


def _expected_current_weather_record():
    return "(14400, 55, 8.84, 1018, 81, 0.59, 106, NULL, NULL, '2022-01-03 14:47:11')"


def _expected_hourly_forecast_record():
    return "(14400, 55, 9.21, 1018, 80, 0.33, 186, 0.21, NULL, '2022-01-03 14:00:00')"


def _expected_daily_forecast_record():
    return "(14400, 55, 9.25, 5.81, 9.4, 1019, 83, 2.72, 79, NULL, NULL, '2022-01-03 12:00:00')"


class TestAddOpenweathermapDataResponseBuilder(TestCase):

# =========== SETUP METHOD
    def setUp(self) -> None:
        self._response_builder = AddOpenWeatherMapDataResponseBuilder(
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


if __name__ == '__main__':
    main()
