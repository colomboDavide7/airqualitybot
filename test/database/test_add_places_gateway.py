# ======================================
# @author:  Davide Colombo
# @date:    2022-01-21, ven, 10:55
# ======================================
from unittest import TestCase, main
from unittest.mock import MagicMock
from airquality.database.gateway import DatabaseGateway
from airquality.datamodel.response import AddPlacesResponse


def _test_database_postal_codes():
    return [("p1",), ("p2",), ("p3",)]


def _test_place_record():
    return "('27100', 'IT', 'Pavia', 'Pavia', 'Lombardia', ST_GeomFromText('POINT(9 45)', 4326))"


def _test_add_places_response():
    return AddPlacesResponse(
        place_record=_test_place_record()
    )


def _mocked_response_builder() -> MagicMock:
    mocked_rb = MagicMock()
    mocked_rb.__len__.return_value = 1
    mocked_rb.__iter__.return_value = [_test_add_places_response()]
    return mocked_rb


class TestDatabaseGatewayAddPlacesSection(TestCase):

# =========== TEST METHODS
    def test_get_existing_poscodes_of_country(self):
        mocked_database_adapt = MagicMock()
        mocked_database_adapt.fetchall.return_value = _test_database_postal_codes()
        gateway = DatabaseGateway(database_adapt=mocked_database_adapt)
        actual = gateway.query_poscodes_of_country(country_code="fakecode")
        self.assertEqual(len(actual), 3)
        self.assertIn("p1", actual)
        self.assertIn("p2", actual)
        self.assertIn("p3", actual)
        self.assertNotIn('p4', actual)

    def test_get_geolocation_of(self):
        mocked_database_adapt = MagicMock()
        mocked_database_adapt.fetchone.return_value = (14400, 9, 45)
        gateway = DatabaseGateway(database_adapt=mocked_database_adapt)
        self._assert_city_data(
            city_data=gateway.query_geolocation_of(
                country_code='fakecode',
                place_name='fakename'
            )
        )

    def test_raise_value_error_when_geolocation_is_none(self):
        mocked_database_adapt = MagicMock()
        mocked_database_adapt.fetchone.return_value = None
        gateway = DatabaseGateway(database_adapt=mocked_database_adapt)
        with self.assertRaises(ValueError):
            gateway.query_geolocation_of(
                country_code='fakecode',
                place_name='fakename'
            )

    def _assert_city_data(self, city_data):
        self.assertEqual(city_data.geoarea_id, 14400)
        self.assertEqual(city_data.longitude, 9)
        self.assertEqual(city_data.latitude, 45)


if __name__ == '__main__':
    main()
