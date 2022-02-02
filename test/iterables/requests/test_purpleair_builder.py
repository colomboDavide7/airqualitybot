# ======================================
# @author:  Davide Colombo
# @date:    2022-01-22, sab, 16:20
# ======================================
import test._test_utils as tutils
from datetime import datetime
from unittest import TestCase, main
from unittest.mock import MagicMock
from airquality.extra.timest import Timest
from airquality.datamodel.request import Channel
from airquality.datamodel.fromapi import PurpleairDM
from airquality.iterables.request_builder import AddPurpleairSensorRequestBuilder


def _test_purpleair_datamodel():
    return PurpleairDM(
        name="fakename",
        sensor_index=9,
        latitude=-74.8888,
        longitude=12.1111,
        primary_id_a=111,
        primary_key_a="key1a",
        primary_id_b=222,
        primary_key_b="key1b",
        secondary_id_a=333,
        secondary_key_a="key2a",
        secondary_id_b=444,
        secondary_key_b="key2b",
        date_created=1234567890
    )


def _mocked_datamodel_builder():
    mocked_db = MagicMock()
    mocked_db.__iter__.return_value = [_test_purpleair_datamodel()]
    return mocked_db


def _expected_sensor_api_param():
    tz = tutils.get_tzinfo_from_coordinates(
        latitude=-74.888,
        longitude=12.1111
    )
    ts = datetime(2009, 2, 13, 23, 31, 30, tzinfo=tz)
    return [
            Channel(api_key="key1a", api_id="111", channel_name="1A", last_acquisition=ts),
            Channel(api_key="key1b", api_id="222", channel_name="1B", last_acquisition=ts),
            Channel(api_key="key2a", api_id="333", channel_name="2A", last_acquisition=ts),
            Channel(api_key="key2b", api_id="444", channel_name="2B", last_acquisition=ts)
        ]


class TestAddPurpleairSensorRequestBuilder(TestCase):

# =========== SETUP METHOD
    def setUp(self) -> None:
        self._builder = AddPurpleairSensorRequestBuilder(
            datamodel=_mocked_datamodel_builder(),
            timest=Timest()
        )

# =========== TEST METHODS
    def test_create_request_for_adding_purpleair_sensor(self):
        self.assertEqual(len(self._builder), 1)
        self._assert_built_request()

# =========== SUPPORT METHODS
    def _assert_built_request(self):
        req1 = self._builder[0]
        self.assertEqual(
            req1.type,
            "Purpleair/Thingspeak"
        )
        self.assertEqual(
            req1.name,
            "fakename (9)"
        )
        self.assertEqual(
            req1.channels,
            _expected_sensor_api_param()
        )


if __name__ == '__main__':
    main()
