# ======================================
# @author:  Davide Colombo
# @date:    2022-02-4, ven, 11:07
# ======================================
from datetime import datetime
from unittest import TestCase, main
from unittest.mock import MagicMock
from airquality.iterables.validator import WeatherDataIterableValidRequests
from airquality.datamodel.requests import AddWeatherDataRequest, WeatherAlertRequest


def _weather_alert_request():
    return [
        WeatherAlertRequest(
            sender='sender',
            event='event',
            begin=datetime(2022, 1, 10, 9, 44),
            until=datetime(2022, 1, 11, 9, 44),
            description=''
        ),
        WeatherAlertRequest(
            sender='new',
            event='new',
            begin=datetime(2022, 2, 10, 9, 44),
            until=datetime(2022, 2, 11, 9, 44),
            description='new'
        )
    ]


def _test_requests():
    return [
        AddWeatherDataRequest(
            current=None,
            hourly=[],
            daily=[],
            alerts=_weather_alert_request()
        )
    ]


def _mocked_requests():
    mocked_rq = MagicMock()
    mocked_rq.__len__.return_value = 1
    mocked_rq.__iter__.return_value = _test_requests()
    return mocked_rq


class mocked_exist_weather_alert(MagicMock):

    def __call__(self, *args, **kwargs):
        geoarea_id = kwargs['geoarea_id']
        alert = args[0]

        if alert.event == 'new' and geoarea_id == 11 and alert.begin == datetime(2022, 2, 10, 9, 44):
            return False
        return True


def _mocked_database_gway():
    mocked_dg = MagicMock()
    mocked_dg.exists_weather_alert_of = mocked_exist_weather_alert()
    return mocked_dg


class TestWeatherDataIterableValidRequests(TestCase):

    def test_validate_weather_data_requests(self):
        mocked_gateway = _mocked_database_gway()
        valid_requests = WeatherDataIterableValidRequests(
            requests=_mocked_requests(),
            fexists=mocked_gateway.exists_weather_alert_of,
            extra={'geoarea_id': 11}
        )
        valid_req = valid_requests[0]
        alerts = valid_req.alerts
        self.assertEqual(len(alerts), 1)
        new_alert = alerts[0]
        self.assertEqual(new_alert.sender, 'new')
        self.assertEqual(new_alert.event, 'new')
        self.assertEqual(new_alert.begin, datetime(2022, 2, 10, 9, 44))


if __name__ == '__main__':
    main()
