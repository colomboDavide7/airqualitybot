# ======================================
# @author:  Davide Colombo
# @date:    2022-01-21, ven, 09:58
# ======================================
from unittest import TestCase, main
from unittest.mock import MagicMock
from airquality.database.gateway import DatabaseGateway
from airquality.datamodel.responses import AddFixedSensorResponse


def _test_database_sensor_names():
    return [("n1",), ("n2",), ("n3",)]


def _expected_sensor_names():
    return {"n1", "n2", "n3"}


def _test_add_fixed_sensors_response():
    return AddFixedSensorResponse(
            sensor_record="(12, 'faketype', 'fakename')",
            apiparam_record="(12, 'key1', 'ident1', 'name1', '2018-12-13 18:19:00'),"
                            "(12, 'key2', 'ident2', 'name2', '2018-12-13 18:19:00')"
        )


def _mocked_response_builder() -> MagicMock:
    mocked_rb = MagicMock()
    mocked_rb.__len__.return_value = 1
    mocked_rb.__iter__.return_value = [_test_add_fixed_sensors_response()]
    return mocked_rb


class TestDatabaseGatewayAddFixedSensorsSection(TestCase):

# =========== TEST METHODS
    def test_get_existing_sensor_names(self):
        mocked_database_adapt = MagicMock()
        mocked_database_adapt.fetchall.return_value = _test_database_sensor_names()
        gateway = DatabaseGateway(database_adapt=mocked_database_adapt)
        self.assertEqual(
            gateway.query_sensor_names_of_type(sensor_type="faketype"),
            _expected_sensor_names()
        )

    def test_get_max_sensor_id_plus_one(self):
        mocked_database_adapt = MagicMock()
        mocked_database_adapt.fetchone.return_value = (12,)
        gateway = DatabaseGateway(database_adapt=mocked_database_adapt)
        self.assertEqual(
            gateway.query_max_sensor_id_plus_one(),
            13
        )

    def test_get_one_when_max_sensor_id_query_return_none(self):
        mocked_database_adapt = MagicMock()
        mocked_database_adapt.fetchone.return_value = (None,)
        gateway = DatabaseGateway(database_adapt=mocked_database_adapt)
        self.assertEqual(
            gateway.query_max_sensor_id_plus_one(),
            1
        )

    def test_query_purpleair_location_valid_location_from_sensor_index(self):
        mocked_database_adapt = MagicMock()
        mocked_database_adapt.fetchone.return_value = (12, 9.12345, 45.02345)
        gateway = DatabaseGateway(database_adapt=mocked_database_adapt)
        geo = gateway.query_purpleair_sensor_location(sensor_index=123)
        self.assertEqual(geo.sensor_id, 12)
        self.assertEqual(geo.latitude, 45.02345)
        self.assertEqual(geo.longitude, 9.12345)

    def test_execute_query(self):
        mocked_database_adapt = MagicMock()
        mocked_database_adapt.execute = MagicMock()
        gateway = DatabaseGateway(database_adapt=mocked_database_adapt)
        gateway.execute(query="fake query;")
        actual_query = mocked_database_adapt.execute.call_args[0][0]
        self.assertEqual(
            actual_query,
            'fake query;'
        )


if __name__ == '__main__':
    main()
