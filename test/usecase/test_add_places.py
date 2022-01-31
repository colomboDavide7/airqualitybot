######################################################
#
# Author: Davide Colombo
# Date: 01/01/22 11:06
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from unittest import TestCase, main
from unittest.mock import MagicMock, patch
from airquality.usecase.add_geonames_places import AddGeonamesPlaces, _fullpath


def _test_directory_content():
    return {"fakefile1.txt", ".ignored_file"}


def _test_database_postal_codes():
    return {'p1', 'p2', 'p3'}


def _mocked_database_gway():
    mocked_gateway = MagicMock()
    mocked_gateway.execute = MagicMock()
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


def _expected_query():
    return "INSERT INTO level0_raw.geographical_area " \
           "(postal_code, country_code, place_name, province, state, geom) " \
           f"VALUES {_expected_add_places_record()};"


class TestAddPlaces(TestCase):

# =========== SETUP METHOD
    def setUp(self) -> None:
        self._mocked_database_gway = _mocked_database_gway()

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
        usecase = AddGeonamesPlaces(database_gway=self._mocked_database_gway)
        usecase.run()
        self._assert_query()
        self._assert_usecase_properties(usecase)

# =========== SUPPORT METHODS
    def _assert_query(self):
        query = self._mocked_database_gway.execute.call_args[1]['query']
        self.assertEqual(
            query,
            _expected_query()
        )

    def _assert_usecase_properties(self, usecase):
        self._assert_directory_filenames(usecase)
        self._assert_existing_postal_codes(usecase)
        self.assertEqual(
            _fullpath("fakefile.txt"),
            'fake_dir/fake_dirr/fake_dirrr/fakefile.txt'
        )

    def _assert_directory_filenames(self, usecase):
        self.assertIn('fakefile1.txt', usecase._filenames)
        self.assertNotIn('.ignored_file', usecase._filenames)

    def _assert_existing_postal_codes(self, usecase):
        self.assertIn('p1', usecase._poscodes_of("fakecountry"))
        self.assertIn('p2', usecase._poscodes_of("fakecountry"))
        self.assertIn('p3', usecase._poscodes_of("fakecountry"))


if __name__ == '__main__':
    main()
