######################################################
#
# Author: Davide Colombo
# Date: 01/01/22 11:06
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from unittest import TestCase, main
from unittest.mock import MagicMock, patch
from airquality.usecase.add_geonames_places import AddGeonamesPlaces


def _test_directory_content():
    return {"fakefile1.txt", ".ignored_file"}


def _test_database_postal_codes():
    return {'p1', 'p2', 'p3'}


def _mocked_database_gway():
    mocked_gateway = MagicMock()
    mocked_gateway.insert_places = MagicMock()
    mocked_gateway.query_poscodes_of_country.return_value = _test_database_postal_codes()
    return mocked_gateway


def _test_country_place_lines():
    with open('test_resources/ES.txt', 'r') as f:
        return f.read()


def _mocked_responses() -> MagicMock:
    mocked_responses = MagicMock()
    mocked_responses.read.side_effect = [_test_country_place_lines()]
    mocked_responses.__enter__.return_value = mocked_responses
    return mocked_responses


def _mocked_environ():
    return {
        'resource_dir': 'fake_dir',
        'geonames_dir': 'fake_dirr',
        'geonames_data_dir': 'fake_dirrr'
    }


def _expected_add_places_record():
    return "('04001', 'ES', 'Almeria', 'Almeria', 'Andalucia', ST_GeomFromText('POINT(-2.4597 36.8381)', 4326))"


class TestAddPlaces(TestCase):

# =========== SETUP METHOD
    def setUp(self) -> None:
        self._mocked_database_gway = _mocked_database_gway()
        self.usecase = AddGeonamesPlaces(
            database_gway=self._mocked_database_gway
        )

# =========== TEST METHODS
    @patch('airquality.environment.os')
    @patch('airquality.usecase.add_geonames_places.listdir')
    @patch('airquality.usecase.add_geonames_places.isfile')
    @patch('airquality.core.apidata_builder.open')
    def test_run_add_fixed_sensors_usecase(self, mocked_open, mocked_isfile, mocked_listdir, mocked_os):
        mocked_os.environ = _mocked_environ()
        mocked_listdir.return_value = _test_directory_content()
        mocked_isfile.return_value = [True, True, True]
        mocked_open.return_value = _mocked_responses()
        self.usecase.run()
        self._assert_responses()
        self._assert_usecase_properties()

# =========== SUPPORT METHODS
    def _assert_responses(self):
        responses = self._mocked_database_gway.insert_places.call_args[0][0]
        self.assertEqual(len(responses), 3)
        self.assertEqual(
            responses[0].place_record,
            _expected_add_places_record()
        )

    def _assert_usecase_properties(self):
        self._assert_directory_filenames()
        self._assert_existing_postal_codes()
        self.assertEqual(
            self.usecase.fullpath("fakefile.txt"),
            'fake_dir/fake_dirr/fake_dirrr/fakefile.txt'
        )

    def _assert_directory_filenames(self):
        self.assertIn('fakefile1.txt', self.usecase.filenames)
        self.assertNotIn('.ignored_file', self.usecase.filenames)

    def _assert_existing_postal_codes(self):
        self.assertIn('p1', self.usecase.poscodes_of("fakecountry"))
        self.assertIn('p2', self.usecase.poscodes_of("fakecountry"))
        self.assertIn('p3', self.usecase.poscodes_of("fakecountry"))


if __name__ == '__main__':
    main()
