# ======================================
# @author:  Davide Colombo
# @date:    2022-01-24, lun, 08:51
# ======================================
from datetime import datetime, timezone
from unittest import TestCase, main
from unittest.mock import MagicMock, patch
from airquality.datamodel.geometry import PostgisPoint
from airquality.iterables.responses import FixedSensorIterableResponses
from airquality.datamodel.requests import AddFixedSensorRequest, SensorChannelParam, SensorInfo


def _test_sensor_location():
    return PostgisPoint(
        latitude=1.234,
        longitude=5.666
    )


def _test_sensor_api_param():
    ts = datetime(2021, 10, 11, 9, 44)
    return [
        SensorChannelParam(api_key="key1a", api_id="111", channel_name="1A", last_acquisition=ts),
        SensorChannelParam(api_key="key1b", api_id="222", channel_name="1B", last_acquisition=ts),
        SensorChannelParam(api_key="key2a", api_id="333", channel_name="2A", last_acquisition=ts),
        SensorChannelParam(api_key="key2b", api_id="444", channel_name="2B", last_acquisition=ts)
    ]


def _test_valid_request():
    return AddFixedSensorRequest(
        basic_info=SensorInfo(type='faketype', name='fakename'),
        channel_param=_test_sensor_api_param()
    )


def _mocked_validator():
    mocked_v = MagicMock()
    mocked_v.__len__.return_value = 1
    mocked_v.__iter__.return_value = [_test_valid_request()]
    return mocked_v


def _mocked_current_utc_timestamp():
    return datetime(2021, 12, 29, 18, 33, tzinfo=timezone.utc)


def _expected_sensor_record():
    return "(12, 'faketype', 'fakename')"


def _expected_sensor_api_param_record():
    ts = "2021-10-11 09:44:00"
    return f"(12, 'key1a', '111', '1A', '{ts}')," \
           f"(12, 'key1b', '222', '1B', '{ts}')," \
           f"(12, 'key2a', '333', '2A', '{ts}')," \
           f"(12, 'key2b', '444', '2B', '{ts}')"


class TestAddPurpleairSensorsResponseBuilder(TestCase):

# =========== TEST METHODS
    @patch('airquality.extra.timest.datetime')
    def test_create_response_to_request_of_adding_fixed_sensor(self, mocked_datetime):
        mocked_datetime.now.return_value = _mocked_current_utc_timestamp()
        response_builder = FixedSensorIterableResponses(
            requests=_mocked_validator(),
            start_sensor_id=12
        )
        self.assertEqual(len(response_builder), 1)
        self._assert_response(record=response_builder[0])

# =========== SUPPORT METHODS
    def _assert_response(self, record):
        self.assertEqual(
            record.sensor_record,
            _expected_sensor_record()
        )
        self.assertEqual(
            record.apiparam_record,
            _expected_sensor_api_param_record()
        )


if __name__ == '__main__':
    main()
