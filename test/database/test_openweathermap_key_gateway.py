######################################################
#
# Author: Davide Colombo
# Date: 30/12/21 14:51
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from unittest import TestCase, main
from unittest.mock import MagicMock
from airquality.database.gateway import DatabaseGateway


def _test_database_openweathermap_keys():
    return [
        ('key1', 0, 60),
        ('key2', 12, 60)
    ]


class TestDatabaseGatewayServiceAPIParamSection(TestCase):

# =========== TEST METHODS
    def test_query_openweathermap_keys(self):
        mocked_database_adapt = MagicMock()
        mocked_database_adapt.fetchall.return_value = _test_database_openweathermap_keys()
        gateway = DatabaseGateway(database_adapt=mocked_database_adapt)
        self._assert_openweathermap_keys(
            key=gateway.query_openweathermap_keys()
        )

    def test_raise_value_error_when_openweathermap_key_table_is_empty(self):
        mocked_database_adapt = MagicMock()
        mocked_database_adapt.fetchall.return_value = []
        gateway = DatabaseGateway(database_adapt=mocked_database_adapt)
        with self.assertRaises(ValueError):
            gateway.query_openweathermap_keys()

    def _assert_openweathermap_keys(self, key):
        self.assertEqual(key[0].key, "key1")
        self.assertEqual(key[0].n_done, 0)
        self.assertEqual(key[1].key, "key2")
        self.assertEqual(key[1].n_done, 12)


if __name__ == '__main__':
    main()
