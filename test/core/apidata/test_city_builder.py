# ======================================
# @author:  Davide Colombo
# @date:    2022-01-22, sab, 16:03
# ======================================
from unittest import TestCase, main
from unittest.mock import MagicMock, patch
from airquality.core.apidata_builder import WeatherCityDataBuilder


def _test_cities_json():
    with open('test_resources/weather_cities.json', 'r') as f:
        return f.read()


def _mocked_opened_file():
    mocked_f = MagicMock()
    mocked_f.__enter__.return_value = mocked_f
    mocked_f.read.return_value = _test_cities_json()
    return mocked_f


class TestWeatherCityDataBuilder(TestCase):

# =========== TEST METHODS
    @patch('airquality.core.apidata_builder.open')
    def test_create_weather_city_data(self, mocked_open):
        mocked_open.return_value = _mocked_opened_file()
        builder = WeatherCityDataBuilder(
            filepath="fakepath"
        )
        self.assertEqual(len(builder), 1)
        self._assert_built_data(datamodel=builder[0])

# =========== SUPPORT METHODS
    def _assert_built_data(self, datamodel):
        self.assertEqual(datamodel.country_code, "IT")
        self.assertEqual(datamodel.place_name, "Pavia")


if __name__ == '__main__':
    main()
