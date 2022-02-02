# ======================================
# @author:  Davide Colombo
# @date:    2022-01-22, sab, 16:45
# ======================================
from datetime import datetime
import test._test_utils as tutils
from unittest import TestCase, main
from unittest.mock import MagicMock
from airquality.extra.timest import thingspeak_timest
from airquality.datamodel.fromapi import ThingspeakDM
from airquality.iterables.requests import ThingspeakIterableRequests


# ================================================================================================== #

#                                   THINGSPEAK PRIMARY CHANNEL A

# ================================================================================================== #
def _test_primary_channel_a_datamodel():
    return ThingspeakDM(
        created_at="2021-12-20T11:18:40Z",
        field1="20.50",
        field2=None,
        field3="37.43",
        field6="55",
        field7="60"
    )


def _test_field_mapping_primary_channel_a():
    return {'field1': 'p1', 'field2': 'p2', 'field3': 'p3', 'field6': 'p6', 'field7': 'p7'}


def _test_measure_param_mapping_primary_channel_a():
    return {'p1': 12, 'p2': 13, 'p3': 14, 'p6': 15, 'p7': 16}


def _mocked_datamodel_builder():
    mocked_db = MagicMock()
    mocked_db.__iter__.return_value = [_test_primary_channel_a_datamodel()]
    return mocked_db


def _expected_acquisition_timestamp():
    ts = tutils.get_tzinfo_from_coordinates(
        latitude=45,
        longitude=9
    )
    return datetime(2021, 12, 20, 12, 18, 40, tzinfo=ts)


def _expected_measures():
    return [(12, 20.50), (14, 37.43), (15, 55), (16, 60)]


class TestAddThingspeakMeasuresRequestBuilder(TestCase):

# =========== SETUP METHOD
    def setUp(self) -> None:
        self._builder = ThingspeakIterableRequests(
            datamodels=_mocked_datamodel_builder(),
            timest=thingspeak_timest(),
            measure_param=_test_measure_param_mapping_primary_channel_a(),
            api_field_names=_test_field_mapping_primary_channel_a()
        )

# =========== TEST METHOD
    def test_create_request_for_adding_thingspeak_primary_channel_a_measures(self):
        self.assertEqual(len(self._builder), 1)
        self._assert_request()

# =========== SUPPORT METHOD
    def _assert_request(self):
        req = self._builder[0]
        self.assertEqual(
            req.timestamp,
            _expected_acquisition_timestamp()
        )
        self.assertEqual(
            req.measures, _expected_measures()
        )

# ================================================================================================== #

#                                   THINGSPEAK PRIMARY CHANNEL B

# ================================================================================================== #


def _test_primary_channel_b_datamodel():
    return ThingspeakDM(
        created_at="2019-02-12T14:33:00Z",
        field1=2.3,
        field2=8.7,
        field3=5.5,
        field6=1014.55
    )


def _test_field_mapping_primary_channel_b():
    return {'field1': 'p1', 'field2': 'p2', 'field3': 'p3', 'field6': 'p6'}


def _test_measure_param_primary_channel_b():
    return {'p1': 12, 'p2': 13, 'p3': 14, 'p6': 19}


def _mocked_primary_channel_b_datamodel_builder():
    mocked_db = MagicMock()
    mocked_db.__iter__.return_value = [_test_primary_channel_b_datamodel()]
    return mocked_db


def _expected_acquisition_timestamp_primary_channel_b():
    tz = tutils.get_tzinfo_from_coordinates(
        latitude=45,
        longitude=9
    )
    return datetime(2019, 2, 12, 15, 33, tzinfo=tz)


def _expected_measures_primary_channel_b():
    return [(12, 2.3), (13, 8.7), (14, 5.5), (19, 1014.55)]


class TestAddThingspeakMeasuresRequestBuilderPrimaryChannelB(TestCase):

# =========== SETUP METHOD
    def setUp(self) -> None:
        self._builder = ThingspeakIterableRequests(
            datamodels=_mocked_primary_channel_b_datamodel_builder(),
            timest=thingspeak_timest(),
            measure_param=_test_measure_param_primary_channel_b(),
            api_field_names=_test_field_mapping_primary_channel_b()
        )

# =========== TEST METHOD
    def test_create_request_for_adding_thingspeak_primary_channel_b_measures(self):
        self.assertEqual(
            len(self._builder),
            1
        )
        self._assert_request()

# =========== SUPPORT METHOD
    def _assert_request(self):
        req = self._builder[0]
        self.assertEqual(
            req.timestamp,
            _expected_acquisition_timestamp_primary_channel_b()
        )
        self.assertEqual(
            req.measures,
            _expected_measures_primary_channel_b()
        )


if __name__ == '__main__':
    main()
