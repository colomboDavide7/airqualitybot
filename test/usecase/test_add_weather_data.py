######################################################
#
# Author: Davide Colombo
# Date: 05/01/22 15:22
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import json
import test._test_utils as tutils
from unittest import TestCase, main
from unittest.mock import MagicMock, patch
from airquality.datamodel.apidata import CityOfGeoarea
from airquality.url.url_reader import URLReader
from airquality.datamodel.openweathermap_key import OpenweathermapKey
from airquality.extra.timest import openweathermap_timest
from airquality.usecase.add_weather_data import AddWeatherData


def _test_weather_conditions():
    return [(55, 804, "04d"), (37, 500, "13d"), (56, 804, "04n")]


def _test_json_response():
    return tutils.get_json_response_from_file(
        filename='openweather_data.json'
    )


def _mocked_responses() -> MagicMock:
    mocked_r = MagicMock()
    mocked_r.content = json.dumps(_test_json_response()).encode('utf-8')
    mocked_r.status_code = 200
    return mocked_r


def _test_cities():
    with open('test_resources/weather_cities.json', 'r') as f:
        return f.read()


def _mocked_city_file() -> MagicMock:
    mocked_f = MagicMock()
    mocked_f.read.return_value = _test_cities()
    mocked_f.__enter__.return_value = mocked_f
    return mocked_f


def _test_opwmap_key():
    return OpenweathermapKey(
        key_value="fakekey",
        done_requests_per_minute=0,
        max_requests_per_minute=60
    )


def _test_database_geolocation_of_city():
    return CityOfGeoarea(
        geoarea_id=14400,
        latitude=0.0,
        longitude=0.0
    )


def _mocked_database_gway() -> MagicMock:
    mocked_gateway = MagicMock()
    mocked_gateway.query_openweathermap_keys.return_value = [_test_opwmap_key()]
    mocked_gateway.query_weather_conditions.return_value = _test_weather_conditions()
    mocked_gateway.query_geolocation_of.return_value = _test_database_geolocation_of_city()
    mocked_gateway.insert_weather_data = MagicMock()
    return mocked_gateway


def _expected_weather_map():
    return {
        804: {
                '04d': 55,
                '04n': 56
            },
        500: {
                "13d": 37
            }
        }


def _expected_current_record():
    return "(14400, 55, 8.84, 1018, 81, 0.59, 106, NULL, NULL, " \
           "'2022-01-03 14:47:11+01:00', '2022-01-03 08:02:17+01:00', '2022-01-03 16:52:55+01:00')"


def _expected_hourly_forecast():
    return "(14400, 55, 9.21, 1018, 80, 0.33, 186, 0.21, 0, NULL, '2022-01-03 14:00:00+01:00')"


def _expected_daily_forecast():
    return "(14400, 55, 9.25, 5.81, 9.4, 1019, 83, 2.72, 79, NULL, 0.01, NULL, '2022-01-03 12:00:00+01:00')"


class AddWeatherDataIntegrationTest(TestCase):

# =========== SETUP METHOD
    def setUp(self) -> None:
        self._mocked_database_gway = _mocked_database_gway()
        self._usecase = AddWeatherData(
            database_gway=self._mocked_database_gway,
            url_reader=URLReader(),
            timest=openweathermap_timest()
        )

# =========== TEST METHOD
    @patch('airquality.environment.os')
    @patch('airquality.core.apidata_builder.open')
    @patch('airquality.url.url_reader.requests.get')
    def test_add_weather_data(self, mocked_get, mocked_open, mocked_os):
        mocked_os.environ = {'openweathermap_url': 'fake_url'}
        mocked_get.return_value = _mocked_responses()
        mocked_open.return_value = _mocked_city_file()
        self._usecase.run()
        self._assert_responses()
        self._assert_usecase_properties()

# =========== SUPPORT METHODS
    def _assert_responses(self):
        responses = self._mocked_database_gway.insert_weather_data.call_args[1]['responses']
        self.assertEqual(len(responses), 1)
        self.assertEqual(
            responses[0].current_weather_record,
            _expected_current_record()
        )
        self.assertEqual(
            responses[0].hourly_forecast_record,
            _expected_hourly_forecast()
        )
        self.assertEqual(
            responses[0].daily_forecast_record,
            _expected_daily_forecast()
        )

    def _assert_usecase_properties(self):
        self.assertEqual(
            self._usecase.weather_map,
            _expected_weather_map()
        )


if __name__ == '__main__':
    main()
