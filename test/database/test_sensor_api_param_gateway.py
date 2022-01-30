# ======================================
# @author:  Davide Colombo
# @date:    2022-01-21, ven, 11:43
# ======================================
from datetime import datetime
from unittest import TestCase, main
from unittest.mock import MagicMock
from airquality.datamodel.apiparam import APIParam
from airquality.database.gateway import DatabaseGateway


def _fake_last_acquisition_datetime():
    return datetime.strptime("2012-09-17 08:37:00", "%Y-%m-%d %H:%M:%S")


def _expected_update_last_acq_query():
    return "UPDATE level0_raw.sensor_api_param " \
           "SET last_acquisition = '2012-09-17 08:37:00' " \
           "WHERE sensor_id = 12 AND ch_name = 'fakename';"


def _test_database_channel_data():
    ts = datetime(2018, 12, 11, 9, 59)
    return [
        (1, 'k1', 'i1', 'n1', ts),
        (1, 'k2', 'i2', 'n2', ts),
        (2, 'z1', 'a1', 'm1', ts)
    ]


def _expected_sensor_api_param():
    ts = datetime(2018, 12, 11, 9, 59)
    return [
        APIParam(sensor_id=1, api_key="k1", api_id="i1", ch_name="n1", last_acquisition=ts),
        APIParam(sensor_id=1, api_key="k2", api_id="i2", ch_name="n2", last_acquisition=ts),
        APIParam(sensor_id=2, api_key="z1", api_id="a1", ch_name="m1", last_acquisition=ts)
    ]


class TestDatabaseGatewaySensorAPIParamSection(TestCase):

# =========== TEST METHODS
    def test_get_last_acquisition_timestamp_of_sensor_channel(self):
        mocked_database_adapt = MagicMock()
        mocked_database_adapt.fetchone.return_value = (_fake_last_acquisition_datetime(),)
        gateway = DatabaseGateway(database_adapt=mocked_database_adapt)
        self.assertEqual(
            gateway.query_last_acquisition_of(sensor_id=12, ch_name="fakename"),
            datetime.strptime("2012-09-17 08:37:00", "%Y-%m-%d %H:%M:%S")
        )

    def test_raise_value_error_when_last_acquisition_timestamp_is_none(self):
        mocked_database_adapt = MagicMock()
        mocked_database_adapt.fetchone.return_value = None
        gateway = DatabaseGateway(database_adapt=mocked_database_adapt)
        with self.assertRaises(ValueError):
            gateway.query_last_acquisition_of(sensor_id=1, ch_name='fakename')

    def test_get_apiparam_of_sensor_type(self):
        mocked_database_adapt = MagicMock()
        mocked_database_adapt.fetchall.return_value = _test_database_channel_data()
        gateway = DatabaseGateway(database_adapt=mocked_database_adapt)
        self.assertEqual(
            gateway.query_sensor_apiparam_of_type(sensor_type="faketype"),
            _expected_sensor_api_param()
        )

    def test_raise_value_error_when_database_sensor_api_param_is_none(self):
        mocked_database_adapt = MagicMock()
        mocked_database_adapt.fetchall.return_value = []
        gateway = DatabaseGateway(database_adapt=mocked_database_adapt)
        with self.assertRaises(ValueError):
            gateway.query_sensor_apiparam_of_type(sensor_type="faketype")


if __name__ == '__main__':
    main()
