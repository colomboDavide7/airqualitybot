# ======================================
# @author:  Davide Colombo
# @date:    2022-01-21, ven, 10:45
# ======================================
from unittest import TestCase, main
from unittest.mock import MagicMock
from airquality.database.gateway import DatabaseGateway
from airquality.datamodel.response import AddStationMeasuresResponse


def _test_measure_record():
    return "(140, 99, 12, 20.5, '2021-12-20 11:18:40'),(140, 99, 13, 35.53, '2021-12-20 11:18:40')," \
           "(140, 99, 14, 37.43, '2021-12-20 11:18:40'),(140, 99, 15, 55, '2021-12-20 11:18:40')," \
           "(140, 99, 16, 60, '2021-12-20 11:18:40')"


def _test_add_station_measures_response():
    return AddStationMeasuresResponse(
        measure_record=_test_measure_record()
    )


def _mocked_response_builder():
    mocked_rb = MagicMock()
    mocked_rb.__len__.return_value = 1
    mocked_rb.__iter__.return_value = [_test_add_station_measures_response()]
    return mocked_rb


def _expected_query():
    return "INSERT INTO level0_raw.station_measurement " \
           "(packet_id, sensor_id, param_id, param_value, timestamp) " \
           f"VALUES {_test_measure_record()};"


class TestDatabaseGatewayAddStationMeasuresSection(TestCase):

# =========== TEST METHODS
    def test_get_max_station_packet_id_plus_one(self):
        mocked_database_adapt = MagicMock()
        mocked_database_adapt.fetchone.return_value = (149,)
        gateway = DatabaseGateway(database_adapt=mocked_database_adapt)
        self.assertEqual(
            gateway.query_max_station_packet_id_plus_one(),
            150
        )

    def test_get_one_when_max_station_packet_id_is_none(self):
        mocked_database_adapt = MagicMock()
        mocked_database_adapt.fetchone.return_value = (None,)
        gateway = DatabaseGateway(database_adapt=mocked_database_adapt)
        self.assertEqual(
            gateway.query_max_station_packet_id_plus_one(),
            1
        )

    def test_insert_station_measures(self):
        mocked_database_adapt = MagicMock()
        mocked_database_adapt.execute = MagicMock()
        gateway = DatabaseGateway(database_adapt=mocked_database_adapt)
        gateway.insert_station_measures(responses=_mocked_response_builder())
        mocked_database_adapt.execute.assert_called_with(_expected_query())


if __name__ == '__main__':
    main()
