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
from airquality.request import AddFixedSensorRequest, AddMobileMeasureRequest, Channel, Geolocation
from airquality.response_builder import AddFixedSensorResponseBuilder, AddMobileMeasureResponseBuilder

SQL_TIMESTAMP_FMT = "%Y-%m-%d %H:%M:%S"


class TestResponseBuilder(TestCase):

    @patch('airquality.response_builder.datetime')
    def test_create_response_to_request_of_adding_fixed_sensor(self, mocked_datetime):
        mocked_now = datetime.strptime("2021-12-29 18:33:00", SQL_TIMESTAMP_FMT)
        mocked_datetime.now.return_value = mocked_now

        test_datetime = datetime.strptime("2021-10-11 09:44:00", SQL_TIMESTAMP_FMT)

        test_channels = [
            Channel(api_key="key1a", api_id="111", channel_name="1A", last_acquisition=test_datetime),
            Channel(api_key="key1b", api_id="222", channel_name="1B", last_acquisition=test_datetime),
            Channel(api_key="key2a", api_id="333", channel_name="2A", last_acquisition=test_datetime),
            Channel(api_key="key2b", api_id="444", channel_name="2B", last_acquisition=test_datetime)
        ]
        test_geolocation = Geolocation(latitude=1.234, longitude=5.666)

        test_response = AddFixedSensorRequest(
            type="faketype",
            name="fakename",
            channels=test_channels,
            geolocation=test_geolocation
        )

        record = AddFixedSensorResponseBuilder(response=test_response, sensor_id=12).build_response()

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

    def test_create_response_to_request_of_adding_mobile_measure(self):
        test_timestamp = datetime.strptime("2021-12-29 18:33:00", SQL_TIMESTAMP_FMT)
        test_geolocation = Geolocation(latitude=45.876, longitude=9.145)
        test_measures = [(66, 0.17), (48, 8), (94, 10), (2, 11), (4, 29), (12, 42), (39, 1004.68)]

        test_response = AddMobileMeasureRequest(
            timestamp=test_timestamp,
            geolocation=test_geolocation,
            measures=test_measures
        )

        record = AddMobileMeasureResponseBuilder(response=test_response, packet_id=12399).build_response()

        expected_timestamp = "2021-12-29 18:33:00"
        expected_geom = "ST_GeomFromText('POINT(9.145 45.876)', 26918)"
        expected_measure_record = f"(12399, 66, '0.17', '{expected_timestamp}', {expected_geom})," \
                                  f"(12399, 48, '8', '{expected_timestamp}', {expected_geom})," \
                                  f"(12399, 94, '10', '{expected_timestamp}', {expected_geom})," \
                                  f"(12399, 2, '11', '{expected_timestamp}', {expected_geom})," \
                                  f"(12399, 4, '29', '{expected_timestamp}', {expected_geom})," \
                                  f"(12399, 12, '42', '{expected_timestamp}', {expected_geom})," \
                                  f"(12399, 39, '1004.68', '{expected_timestamp}', {expected_geom})"

        self.assertEqual(record.measure_record, expected_measure_record)


if __name__ == '__main__':
    main()
