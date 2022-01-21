######################################################
#
# Author: Davide Colombo
# Date: 05/01/22 15:22
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import test._test_utils as tutils
from unittest import TestCase, main
from unittest.mock import MagicMock, patch
from airquality.url.api_server_wrap import APIServerWrapper
from airquality.datamodel.service_param import ServiceParam
from airquality.datamodel.apidata import CityOfGeoarea
from airquality.usecase.add_weather_data import AddWeatherData


class TestAddWeatherDataUsecase(TestCase):

    @patch('airquality.core.apidata_builder.open')
    @patch('airquality.url.api_server_wrap.requests.get')
    def test_add_weather_data(self, mocked_get, mocked_open):
        test_json_response = tutils.get_json_response_from_file(filename='openweather_data.json')

        mocked_api_resp = MagicMock()
        mocked_api_resp.json.return_value = test_json_response
        mocked_get.return_value = mocked_api_resp

        with open('test_resources/weather_cities.json', 'r') as city_file:
            cities = city_file.read()

        mocked_file_resp = MagicMock()
        mocked_file_resp.read.return_value = cities
        mocked_file_resp.__enter__.return_value = mocked_file_resp
        mocked_open.return_value = mocked_file_resp

        test_weather_conditions = [(55, 804, "04d"), (37, 500, "13d"), (56, 804, "04n")]
        expected_weather_conditions = {804: {'04d': 55, '04n': 56}, 500: {"13d": 37}}
        mocked_gateway = MagicMock()
        mocked_gateway.get_service_apiparam_of.return_value = [ServiceParam(api_key="fakekey", n_requests=0)]
        mocked_gateway.query_weather_conditions.return_value = test_weather_conditions
        mocked_gateway.get_service_id_from_name.return_value = 1
        mocked_gateway.query_geolocation_of.return_value = CityOfGeoarea(geoarea_id=14400, latitude=0.0, longitude=0.0)
        mocked_gateway.insert_weather_data = MagicMock()

        usecase = AddWeatherData(
            database_gway=mocked_gateway,
            server_wrap=APIServerWrapper(),
            input_url_template="fakeurl"
        )
        self.assertEqual(usecase.weather_map, expected_weather_conditions)

        usecase.run()
        responses = mocked_gateway.insert_weather_data.call_args[1]['responses']
        self.assertEqual(len(responses), 1)

        resp = responses[0]
        expected_current_record = "(1, 14400, 55, 8.84, 1018, 81, 0.59, 106, NULL, NULL, '2022-01-03 14:47:11')"
        self.assertEqual(resp.current_weather_record, expected_current_record)

        expected_hourly_record = "(1, 14400, 55, 9.21, 1018, 80, 0.33, 186, 0.21, NULL, '2022-01-03 14:00:00')"
        self.assertEqual(resp.hourly_forecast_record, expected_hourly_record)

        expected_daily_record = "(1, 14400, 55, 9.25, 5.81, 9.4, 1019, 83, 2.72, 79, NULL, NULL, '2022-01-03 12:00:00')"
        self.assertEqual(resp.daily_forecast_record, expected_daily_record)


if __name__ == '__main__':
    main()
