# ======================================
# @author:  Davide Colombo
# @date:    2022-01-24, lun, 10:07
# ======================================
from unittest import TestCase, main
from unittest.mock import MagicMock
from airquality.datamodel.geometry import PostgisPoint
from airquality.datamodel.request import AddPlacesRequest
from airquality.core.response_builder import AddPlacesResponseBuilder


def _test_place_location():
    return PostgisPoint(
        latitude=45,
        longitude=9,
        srid=4326
    )


def _test_request():
    return AddPlacesRequest(
        placename="Pavia",
        poscode="27100",
        state="Lombardia",
        countrycode="IT",
        province="Pavia",
        geolocation=_test_place_location()
    )


def _mocked_validator():
    mocked_v = MagicMock()
    mocked_v.__len__.return_value = 1
    mocked_v.__iter__.return_value = [_test_request()]
    return mocked_v


def _expected_place_record():
    geom = "ST_GeomFromText('POINT(9 45)', 4326)"
    return f"(1, '27100', 'IT', 'Pavia', 'Pavia', 'Lombardia', {geom})"


class TestAddPlacesResponseBuilder(TestCase):

# =========== SETUP METHOD
    def setUp(self) -> None:
        self._response_builder = AddPlacesResponseBuilder(
            requests=_mocked_validator(),
            service_id=1
        )

# =========== TEST METHOD
    def test_create_response_to_request_of_adding_places(self):
        self.assertEqual(
            len(self._response_builder),
            1
        )
        self.assertEqual(
            self._response_builder[0].place_record,
            _expected_place_record()
        )


if __name__ == '__main__':
    main()
