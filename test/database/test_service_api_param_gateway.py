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


def _test_database_service_api_param():
    return [
        ('key1', 0),
        ('key2', 12)
    ]


class TestDatabaseGatewayServiceAPIParamSection(TestCase):

# =========== TEST METHODS
    def test_get_service_id_from_service_name(self):
        mocked_database_adapt = MagicMock()
        mocked_database_adapt.fetchone.return_value = (1, )
        gateway = DatabaseGateway(database_adapt=mocked_database_adapt)
        self.assertEqual(
            gateway.query_service_id_from_name(service_name="fakename"),
            1
        )

    def test_raise_value_error_when_service_id_is_none(self):
        mocked_database_adapt = MagicMock()
        mocked_database_adapt.fetchone.return_value = None
        gateway = DatabaseGateway(database_adapt=mocked_database_adapt)
        with self.assertRaises(ValueError):
            gateway.query_service_id_from_name(service_name="fakename")

    def test_get_service_apiparam(self):
        mocked_database_adapt = MagicMock()
        mocked_database_adapt.fetchall.return_value = _test_database_service_api_param()
        gateway = DatabaseGateway(database_adapt=mocked_database_adapt)
        self._assert_service_api_param(
            api_param=gateway.query_service_apiparam_of(
                service_name="fakename"
            )
        )

    def test_raise_value_error_when_service_api_param_is_empty(self):
        mocked_database_adapt = MagicMock()
        mocked_database_adapt.fetchall.return_value = []
        gateway = DatabaseGateway(database_adapt=mocked_database_adapt)
        with self.assertRaises(ValueError):
            gateway.query_service_apiparam_of(service_name="fakename")

    def _assert_service_api_param(self, api_param):
        self.assertEqual(api_param[0].api_key, "key1")
        self.assertEqual(api_param[0].n_requests, 0)
        self.assertEqual(api_param[1].api_key, "key2")
        self.assertEqual(api_param[1].n_requests, 12)


if __name__ == '__main__':
    main()
