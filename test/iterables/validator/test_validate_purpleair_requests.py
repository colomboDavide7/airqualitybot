# ======================================
# @author:  Davide Colombo
# @date:    2022-01-24, lun, 08:18
# ======================================
from datetime import datetime
from unittest import TestCase, main
from unittest.mock import MagicMock
from airquality.datamodel.geometry import PostgisPoint
from airquality.iterables.validator import AddFixedSensorRequestValidator
from airquality.datamodel.requests import AddFixedSensorRequest, SensorChannelParam


def _test_sensor_location():
    return PostgisPoint(
        latitude=11,
        longitude=-9
    )


def _test_requests_sensor_names():
    return [
        'fakename1',
        'fakename2'
    ]


def _test_last_acquisition_timestamp():
    return datetime.strptime("2021-10-11 09:44:00", "%Y-%m-%d %H:%M:%S")


def _test_sensor_channels():
    return [SensorChannelParam(api_key="k",
                               api_id="i",
                               channel_name="n",
                               last_acquisition=_test_last_acquisition_timestamp())]


def _test_requests():
    return [AddFixedSensorRequest(name=name,
                                  type='faketype',
                                  channel_param=_test_sensor_channels()) for name in _test_requests_sensor_names()]


def _mocked_request_builder():
    mocked_rb = MagicMock()
    mocked_rb.__len__.return_value = len(_test_requests_sensor_names())
    mocked_rb.__iter__.return_value = _test_requests()
    return mocked_rb


def _test_database_sensor_names():
    return {
        'fakename2',
    }


class TestAddPurpleairSensorsRequestsValidator(TestCase):

# =========== SETUP METHOD
    def setUp(self) -> None:
        self._validator = AddFixedSensorRequestValidator(
            request=_mocked_request_builder(),
            name2remove=_test_database_sensor_names()
        )

# =========== TEST METHODS
    def test_validate_add_purpleair_sensor_request(self):
        self.assertEqual(len(self._validator), 1)
        self._assert_valid_requests()

# =========== SUPPORT METHODS
    def _assert_valid_requests(self):
        req = self._validator[0]
        self.assertEqual(req.name, "fakename1")
        self.assertEqual(req.type, "faketype")


if __name__ == '__main__':
    main()
