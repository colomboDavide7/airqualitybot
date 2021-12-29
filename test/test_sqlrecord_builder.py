######################################################
#
# Author: Davide Colombo
# Date: 29/12/21 18:18
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from datetime import datetime
from unittest import TestCase, main
from unittest.mock import patch
from airquality.response import AddFixedSensorResponse, Channel, Geolocation
from airquality.sqlrecord_builder import FixedSensorSQLRecordBuilder


class TestSQLRecordBuilder(TestCase):

    @patch('airquality.sqlrecord_builder.datetime')
    def test_create_fixed_sensor_sql_record(self, mocked_datetime):
        mocked_now = datetime.strptime("2021-12-29 18:33:00", "%Y-%m-%d %H:%M:%S")
        mocked_datetime.now.return_value = mocked_now

        test_datetime = datetime.strptime("2021-10-11 09:44:00", "%Y-%m-%d %H:%M:%S")

        test_channels = [
            Channel(api_key="key1a", api_id="111", channel_name="1A", last_acquisition=test_datetime),
            Channel(api_key="key1b", api_id="222", channel_name="1B", last_acquisition=test_datetime),
            Channel(api_key="key2a", api_id="333", channel_name="2A", last_acquisition=test_datetime),
            Channel(api_key="key2b", api_id="444", channel_name="2B", last_acquisition=test_datetime)
        ]
        test_geolocation = Geolocation(latitude=1.234, longitude=5.666)

        test_response = AddFixedSensorResponse(
            type="faketype",
            name="fakename",
            channels=test_channels,
            geolocation=test_geolocation
        )

        record = FixedSensorSQLRecordBuilder(response=test_response, sensor_id=12).build_sqlrecord()

        expected_datetime = "2021-10-11 09:44:00"
        expected_apiparam_record = f"(12, 'key1a', '111', '1A', '{expected_datetime}')," \
                                   f"(12, 'key1b', '222', '1B', '{expected_datetime}')," \
                                   f"(12, 'key2a', '333', '2A', '{expected_datetime}')," \
                                   f"(12, 'key2b', '444', '2B', '{expected_datetime}')"

        expected_geometry = "ST_GeomFromText('POINT(5.666 1.234)', 26918)"
        expected_geolocation_record = f"(12, '{mocked_now}', NULL, {expected_geometry})"

        self.assertEqual(record.sensor_record, "(12, 'faketype', 'fakename')")
        self.assertEqual(record.apiparam_record, expected_apiparam_record)
        self.assertEqual(record.geolocation_record, expected_geolocation_record)


if __name__ == '__main__':
    main()
