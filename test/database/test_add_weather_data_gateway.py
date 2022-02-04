# ======================================
# @author:  Davide Colombo
# @date:    2022-01-21, ven, 11:24
# ======================================
from datetime import datetime
from unittest import TestCase, main
from unittest.mock import MagicMock
from airquality.database.gateway import DatabaseGateway
from airquality.datamodel.requests import WeatherAlertRequest
from airquality.datamodel.responses import AddWeatherDataResponse


def _expected_delete_hourly_forecast_query():
    return "DELETE FROM level0_raw.hourly_forecast;"


def _expected_delete_daily_forecast_query():
    return "DELETE FROM level0_raw.daily_forecast;"


def _test_database_weather_conditions():
    return [
        (55, 804, '04d'),
        (37, 500, '13d'),
        (56, 804, '04n')
    ]


def _expected_weather_map():
    return {'804_04d': 55, '500_13d': 37, '804_04n': 56}


def _test_current_weather_record():
    return "(14400, 55, 8.84, 1018, 81, 0.59, 106, NULL, NULL, '2022-01-03 14:47:11')"


def _test_hourly_forecast_record():
    return "(14400, 55, 9.21, 1018, 80, 0.33, 186, 0.21, NULL, '2022-01-03 14:00:00')"


def _test_daily_forecast_record():
    return "(14400, 55, 9.25, 5.81, 9.4, 1019, 83, 2.72, 79, NULL, NULL, '2022-01-03 12:00:00')"


def _test_weather_alert_record():
    return "(14400, 'Fake sender', 'Fake event', " \
           "'2022-01-24 19:00:00+01:00', '2022-01-25 09:59:00+01:00', " \
           "'Fake description')"


def _test_add_weather_data_response():
    return AddWeatherDataResponse(
        current_weather_record=_test_current_weather_record(),
        hourly_forecast_record=_test_hourly_forecast_record(),
        daily_forecast_record=_test_daily_forecast_record(),
        weather_alert_record=_test_weather_alert_record()
    )


def _mocked_response_builder() -> MagicMock:
    mocked_rb = MagicMock()
    mocked_rb.__len__.return_value = 1
    mocked_rb.__iter__.return_value = [_test_add_weather_data_response()]
    return mocked_rb


def _test_existing_weather_alert_record():
    return 11111, \
           'sender', \
           'event', \
           datetime(2022, 1, 10, 9, 45), \
           datetime(2022, 1, 10, 17, 15), \
           ''


class TestDatabaseGatewayAddWeatherDataSection(TestCase):

# =========== TEST METHODS
    def test_get_weather_conditions(self):
        mocked_database_adapt = MagicMock()
        mocked_database_adapt.fetchall.return_value = _test_database_weather_conditions()
        gateway = DatabaseGateway(database_adapt=mocked_database_adapt)
        self.assertEqual(
            gateway.query_weather_conditions(),
            _expected_weather_map()
        )

    def test_raise_value_error_when_weather_conditions_are_empty(self):
        mocked_database_adapt = MagicMock()
        mocked_database_adapt.fetchall.return_value = []
        gateway = DatabaseGateway(database_adapt=mocked_database_adapt)
        with self.assertRaises(ValueError):
            gateway.query_weather_conditions()

    def test_true_when_already_exists_weather_alert_record(self):
        mocked_database_adapt = MagicMock()
        mocked_database_adapt.fetchone.return_value = _test_existing_weather_alert_record()
        gateway = DatabaseGateway(database_adapt=mocked_database_adapt)
        self.assertTrue(
            gateway.exists_weather_alert_of(geoarea_id=0,
                                            alert=WeatherAlertRequest(
                                                sender='sender',
                                                event='event',
                                                begin=datetime(2022, 1, 10, 9, 45),
                                                until=datetime(2022, 1, 10, 17, 15),
                                                description=""
                                            ))
        )

    def test_false_when_weather_alert_record_does_not_exist(self):
        mocked_database_adapt = MagicMock()
        mocked_database_adapt.fetchone.return_value = None
        gateway = DatabaseGateway(database_adapt=mocked_database_adapt)
        self.assertFalse(
            gateway.exists_weather_alert_of(geoarea_id=0,
                                            alert=WeatherAlertRequest(
                                                sender='sender',
                                                event='event',
                                                begin=datetime(2022, 1, 10, 9, 45),
                                                until=datetime(2022, 1, 10, 17, 15),
                                                description=""
                                            ))
        )


if __name__ == '__main__':
    main()
