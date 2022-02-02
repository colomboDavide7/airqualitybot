# ======================================
# @author:  Davide Colombo
# @date:    2022-01-21, ven, 10:45
# ======================================
from unittest import TestCase, main
from unittest.mock import MagicMock
from airquality.database.gateway import DatabaseGateway
from airquality.datamodel.fromdb import SensorInfoDM
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


def _expected_fixed_sensor_unique_info():
    return SensorInfoDM(
        sensor_id=0,
        sensor_name='fake_name',
        sensor_lng=-9,
        sensor_lat=44
    )


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

    def test_query_fixed_sensor_unique_info(self):
        mocked_database_adapt = MagicMock()
        mocked_database_adapt.fetchone.return_value = (0, 'fake_name', -9, 44)
        gateway = DatabaseGateway(database_adapt=mocked_database_adapt)
        ident = gateway.query_fixed_sensor_unique_info(sensor_id=0)
        self.assertEqual(ident.sensor_id, 0)
        self.assertEqual(ident.sensor_name, 'fake_name')
        self.assertEqual(ident.sensor_lng, -9.0)
        self.assertEqual(ident.sensor_lat, 44.0)


if __name__ == '__main__':
    main()
