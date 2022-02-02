# ======================================
# @author:  Davide Colombo
# @date:    2022-01-22, sab, 17:12
# ======================================
from unittest import TestCase, main
from unittest.mock import MagicMock
from airquality.datamodel.fromfile import GeonamesDM
from airquality.datamodel.geometry import PostgisPoint
from airquality.iterables.request_builder import AddPlacesRequestBuilder


def _test_geonames_datamodel():
    line = [
        "IT",
        "27100",
        "Pavia'",
        "Lombardia'",
        "statecode",
        "Pavia'",
        "PV",
        "community",
        "communitycode",
        "45",
        "9",
        "4"
    ]
    return GeonamesDM(*line)


def _mocked_datamodel_builder():
    mocked_db = MagicMock()
    mocked_db.__len__.return_value = 1
    mocked_db.__iter__.return_value = [_test_geonames_datamodel()]
    return mocked_db


def _expected_place_geolocation():
    return PostgisPoint(latitude=45, longitude=9, srid=4326)


class TestAddPlacesRequestBuilder(TestCase):

# =========== SETUP METHOD
    def setUp(self) -> None:
        self._builder = AddPlacesRequestBuilder(
            datamodels=_mocked_datamodel_builder()
        )

# =========== TEST METHOD
    def test_create_requests_for_adding_places(self):
        self.assertEqual(
            len(self._builder),
            1
        )
        self._assert_request()

# =========== SUPPORT METHOD
    def _assert_request(self):
        req = self._builder[0]
        self.assertEqual(req.poscode, "27100")
        self.assertEqual(req.placename, "Pavia")
        self.assertEqual(req.state, "Lombardia")
        self.assertEqual(req.province, "Pavia")
        self.assertEqual(req.countrycode, "IT")
        self.assertEqual(req.geolocation, _expected_place_geolocation())


if __name__ == '__main__':
    main()
