# ======================================
# @author:  Davide Colombo
# @date:    2022-01-21, ven, 10:28
# ======================================
from unittest import TestCase, main
from unittest.mock import MagicMock
from airquality.database.gateway import DatabaseGateway
from airquality.datamodel.response import AddMobileMeasureResponse


def _test_database_measure_param():
    return [(1, 'c1'), (2, 'c2')]


def _expected_queried_measure_param():
    return {'c1': 1, 'c2': 2}


def _test_mobile_record():
    return "(13, 1, '0.17', '2021-10-11 09:44:00', ST_GeomFromText('POINT(-12 37)', 26918)), " \
           "(13, 2, '8', '2021-10-11 09:44:00', ST_GeomFromText('POINT(-12.09 37.11)', 26918)), " \
           "(13, 6, '24', '2021-10-11 09:44:00', ST_GeomFromText('POINT(-12.34 37.87)', 26918))"


def _test_add_mobile_measures_response():
    return AddMobileMeasureResponse(
        measure_record=_test_mobile_record()
    )


def _mocked_response_builder() -> MagicMock:
    mocked_rb = MagicMock()
    mocked_rb.__len__.return_value = 1
    mocked_rb.__iter__.return_value = [_test_add_mobile_measures_response()]
    return mocked_rb


def _expected_insert_mobile_measures_query():
    return "INSERT INTO level0_raw.mobile_measurement " \
           "(packet_id, param_id, param_value, timestamp, geom) " \
           f"VALUES {_test_mobile_record()};"


class TestDatabaseGatewayAddMobileMeasuresSection(TestCase):

# =========== TEST METHODS
    def test_get_measure_param_owned_by(self):
        mocked_database_adapt = MagicMock()
        mocked_database_adapt.fetchall.return_value = _test_database_measure_param()
        gateway = DatabaseGateway(database_adapt=mocked_database_adapt)
        self.assertEqual(
            gateway.query_measure_param_owned_by(owner="fakeowner"),
            _expected_queried_measure_param()
        )

    def test_raise_value_error_when_queried_measure_param_is_empty(self):
        mocked_database_adapt = MagicMock()
        mocked_database_adapt.fetchall.return_value = []
        gateway = DatabaseGateway(database_adapt=mocked_database_adapt)
        with self.assertRaises(ValueError):
            gateway.query_measure_param_owned_by(owner="fakeowner")

    def test_insert_mobile_sensor_measures(self):
        mocked_database_adapt = MagicMock()
        mocked_database_adapt.execute = MagicMock()
        gateway = DatabaseGateway(database_adapt=mocked_database_adapt)
        gateway.insert_mobile_measures(responses=_mocked_response_builder())
        mocked_database_adapt.execute.assert_called_with(_expected_insert_mobile_measures_query())

    def test_get_max_mobile_packet_id_plus_one(self):
        mocked_database_adapt = MagicMock()
        mocked_database_adapt.fetchone.return_value = (12399,)
        gateway = DatabaseGateway(database_adapt=mocked_database_adapt)
        self.assertEqual(
            gateway.query_max_mobile_packet_id_plus_one(),
            12400
        )

    def test_query_one_when_max_packet_id_is_none(self):
        mocked_database_adapt = MagicMock()
        mocked_database_adapt.fetchone.return_value = (None,)
        gateway = DatabaseGateway(database_adapt=mocked_database_adapt)
        self.assertEqual(
            gateway.query_max_mobile_packet_id_plus_one(),
            1
        )


if __name__ == '__main__':
    main()
