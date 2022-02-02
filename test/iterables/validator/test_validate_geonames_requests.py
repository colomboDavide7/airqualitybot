######################################################
#
# Author: Davide Colombo
# Date: 30/12/21 08:56
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from unittest import TestCase, main
from unittest.mock import MagicMock
from airquality.datamodel.geometry import PostgisPoint
from airquality.datamodel.requests import AddPlaceRequest
from airquality.iterables.request_validator import AddPlacesRequestValidator


def _test_place_geolocation():
    return PostgisPoint(
        latitude=45,
        longitude=9,
        srid=4326
    )


def _test_request():
    return AddPlaceRequest(
        placename="fakename",
        poscode="fakecode",
        state="fakestate",
        countrycode="fakecode",
        province="fake_province",
        geolocation=_test_place_geolocation()
    )


def _mocked_request_builder():
    mocked_rb = MagicMock()
    mocked_rb.__len__.return_value = 1
    mocked_rb.__iter__.return_value = [_test_request()]
    return mocked_rb


def _test_database_postal_codes():
    return {
        'fakecode',
    }


class TestAddPlacesRequestsValidator(TestCase):

# =========== SETUP METHOD
    def setUp(self) -> None:
        self._validator = AddPlacesRequestValidator(
            requests=_mocked_request_builder(),
            existing_poscodes=_test_database_postal_codes()
        )

# =========== TEST METHODS
    def test_validate_add_places_request(self):
        self.assertEqual(
            len(self._validator),
            0
        )


if __name__ == '__main__':
    main()
