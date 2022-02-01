# ======================================
# @author:  Davide Colombo
# @date:    2022-02-1, mar, 10:15
# ======================================
from datetime import datetime
import test._test_utils as tutils
from unittest import TestCase, main
from unittest.mock import MagicMock, patch
from airquality.datamodel.geolocation import Geolocation
from airquality.usecase.update_purpleair_locations import UpdatePurpleairLocation


def _test_queried_locations():
    return [
        Geolocation(row=(12, 9.44, 45.99)),
        Geolocation(row=(7, 8.78886, 46.82134)),
    ]


def _mocked_database_gateway():
    mocked_dg = MagicMock()
    mocked_dg.execute = MagicMock()
    mocked_dg.query_purpleair_location_of.side_effect = _test_queried_locations()
    return mocked_dg


def _test_json_api_response():
    return b'{"fields": ["sensor_index", "longitude", "latitude"], ' \
           b'"data": [' \
           b'[11111, 8.13, 47.23],' \
           b'[22222, 8.78889541, 46.82134421]' \
           b']}'


def _mocked_json_api_responses():
    mocked_resp = MagicMock()
    mocked_resp.status_code = 200
    mocked_resp.content = _test_json_api_response()
    return mocked_resp


def _test_tzinfo():
    return tutils.get_tzinfo_from_timezone_name(tzname='Europe/Rome')


def _mocked_now():
    return datetime(2022, 1, 22, 10, 37, tzinfo=_test_tzinfo())


def _expected_update_insert_query():
    ts = '2022-01-22 10:37:00+01:00'
    geom = "ST_GeomFromText('POINT(8.13 47.23)', 4326)"
    return f"UPDATE level0_raw.sensor_at_location SET valid_to = '{ts}' WHERE sensor_id = 12 AND valid_to IS NULL;" \
           f"INSERT INTO level0_raw.sensor_at_location (sensor_id, valid_from, geom) VALUES (12, '{ts}', {geom});"


class TestUpdatePurpleairLocationsUsecase(TestCase):

    @patch('airquality.extra.timest.datetime')
    @patch('airquality.url.url_reader.requests.get')
    def test_update_purpleair_locations(self, mocked_get, mocked_datetime):
        mocked_datetime.now.return_value = _mocked_now()
        mocked_get.return_value = _mocked_json_api_responses()
        mocked_database_gway = _mocked_database_gateway()
        usecase = UpdatePurpleairLocation(database_gway=mocked_database_gway)
        usecase.run()

        query = mocked_database_gway.execute.call_args[1]['query']
        self.assertEqual(
            query,
            _expected_update_insert_query()
        )

        mocked_database_gway.execute.assert_called_once()


if __name__ == '__main__':
    main()
