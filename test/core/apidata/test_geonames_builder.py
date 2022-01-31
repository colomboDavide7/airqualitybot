# ======================================
# @author:  Davide Colombo
# @date:    2022-01-22, sab, 15:57
# ======================================
from unittest import TestCase, main
from unittest.mock import MagicMock, patch
from airquality.core.apidata_builder import GeonamesDataBuilder


def _test_file_lines():
    with open('test_resources/ES.txt', 'r') as rf:
        return rf.read()


def _mocked_opened_file():
    mocked_f = MagicMock()
    mocked_f.read.side_effect = [_test_file_lines()]
    mocked_f.__enter__.return_value = mocked_f
    return mocked_f


class TestGeonamesLineDataBuilder(TestCase):

# =========== TEST METHODS
    @patch('airquality.core.apidata_builder.open')
    def test_create_geonames_spain_data(self, mocked_open):
        mocked_open.return_value = _mocked_opened_file()
        builder = GeonamesDataBuilder(
            filepath="fake_filepath"
        )
        self.assertEqual(len(builder), 1)
        self._assert_built_data(datamodel=builder[0])

# =========== SUPPORT METHODS
    def _assert_built_data(self, datamodel):
        self.assertEqual(datamodel.place_name, "Almeria")
        self.assertEqual(datamodel.postal_code, "04001")
        self.assertEqual(datamodel.country_code, "ES")
        self.assertEqual(datamodel.state, "Andalucia")
        self.assertEqual(datamodel.province, "Almeria")
        self.assertEqual(datamodel.latitude, 36.8381)
        self.assertEqual(datamodel.longitude, -2.4597)


if __name__ == '__main__':
    main()
