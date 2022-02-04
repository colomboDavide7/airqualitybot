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
from airquality.datamodel.fromdb import GeoareaLocationDM, OpenweathermapKeyDM
from airquality.usecase.openweathermap import AddWeatherData


def _test_weather_conditions():
    return {
        '804_04d': 55,
        '500_13d': 37,
        '804_04n': 56
    }


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
    return OpenweathermapKeyDM(
        key="fakekey",
        n_done=0,
        n_max=60
    )


def _test_database_geolocation_of_city():
    return GeoareaLocationDM(
        id=14400,
        latitude=0.0,
        longitude=0.0
    )


def _mocked_database_gway() -> MagicMock:
    mocked_gateway = MagicMock()
    mocked_gateway.query_openweathermap_keys.return_value = [_test_opwmap_key()]
    mocked_gateway.query_weather_conditions.return_value = _test_weather_conditions()
    mocked_gateway.query_place_location.return_value = _test_database_geolocation_of_city()
    mocked_gateway.execute = MagicMock()
    return mocked_gateway


def _expected_current_record():
    return "(14400,55,8.84,1018,81,0.59,106,NULL,NULL," \
           "'2022-01-03 14:47:11+01:00','2022-01-03 08:02:17+01:00','2022-01-03 16:52:55+01:00')"


def _expected_hourly_forecast():
    return "(14400,55,9.21,1018,80,0.33,186,0.21,0,NULL,'2022-01-03 14:00:00+01:00')"


def _expected_daily_forecast():
    return "(14400,55,9.25,5.81,9.4,1019,83,2.72,79,NULL,0.01,NULL,'2022-01-03 12:00:00+01:00')"


def _expected_weather_alarm_record():
    return "(14400,'Fake sender','Fake event'," \
           "'2022-01-24 19:00:00+01:00','2022-01-25 09:59:00+01:00','Fake description')"


def _expected_insert_query():
    return "INSERT INTO level0_raw.current_weather " \
            "(geoarea_id, weather_id, temperature, pressure, humidity, wind_speed, " \
            "wind_direction, rain, snow, timestamp, sunrise, sunset) " \
            f"VALUES {_expected_current_record()};" \
            "INSERT INTO level0_raw.hourly_forecast " \
            "(geoarea_id, weather_id, temperature, pressure, humidity, " \
            "wind_speed, wind_direction, rain, pop, snow, timestamp) " \
            f"VALUES {_expected_hourly_forecast()};" \
           "INSERT INTO level0_raw.daily_forecast " \
           "(geoarea_id, weather_id, temperature, min_temp, max_temp, pressure, " \
           "humidity, wind_speed, wind_direction, rain, pop, snow, timestamp) " \
           f"VALUES {_expected_daily_forecast()};" \
           "INSERT INTO level0_raw.weather_alert " \
           "(geoarea_id, sender_name, alert_event, " \
           "alert_begin, alert_until, description) " \
           f"VALUES {_expected_weather_alarm_record()};"


class AddWeatherDataIntegrationTest(TestCase):

# =========== SETUP METHOD
    def setUp(self) -> None:
        self._mocked_database_gway = _mocked_database_gway()
        self._usecase = AddWeatherData(database_gway=self._mocked_database_gway)

# =========== TEST METHOD
    @patch('airquality.environment.os')
    @patch('airquality.iterables.fromapi.open')
    @patch('airquality.extra.url.requests.get')
    def test_add_weather_data(self, mocked_get, mocked_open, mocked_os):
        mocked_os.environ = {'openweathermap_url': 'fake_url'}
        mocked_get.return_value = _mocked_responses()
        mocked_open.return_value = _mocked_city_file()
        self._usecase.execute()
        self._assert_query()
        self._assert_usecase_properties()

# =========== SUPPORT METHODS
    def _assert_query(self):
        query = self._mocked_database_gway.execute.call_args[1]['query']
        self.assertEqual(
            query,
            _expected_insert_query()
        )

    def _assert_usecase_properties(self):
        self.assertEqual(
            self._usecase._weather_map,
            _test_weather_conditions()
        )


if __name__ == '__main__':
    main()
