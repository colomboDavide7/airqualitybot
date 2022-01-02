######################################################
#
# Author: Davide Colombo
# Date: 31/12/21 11:43
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from datetime import datetime
from unittest import TestCase, main
from unittest.mock import MagicMock
from airquality.datamodel.apiparam import APIParam
from airquality.datamodel.geometry import PostgisPoint
from airquality.datamodel.request import AddMobileMeasuresRequest
from airquality.usecase.add_mobile_measures import AddMobileMeasures


class TestAddMobileMeasuresUsecase(TestCase):

    @property
    def get_test_timestamp(self):
        return datetime.strptime("2021-08-10T23:59:00.000Z", "%Y-%m-%dT%H:%M:%S.000Z")

    @property
    def get_test_measures(self):
        return [(66, 0.17), (48, 8), (94, 10), (2, 11), (4, 29), (12, 42), (39, 1004.68)]

    @property
    def get_test_geolocation(self):
        return PostgisPoint(latitude=45.765, longitude=9.897)

    @property
    def get_test_atmotube_request(self):
        return AddMobileMeasuresRequest(
            timestamp=self.get_test_timestamp,
            measures=self.get_test_measures,
            geolocation=self.get_test_geolocation
        )

    def test_add_mobile_measures(self):
        mocked_request_builder = MagicMock()
        mocked_request_builder.__len__.return_value = 1
        mocked_request_builder.__iter__.return_value = [self.get_test_atmotube_request]

        mocked_database_gateway = MagicMock()
        mocked_database_gateway.insert_mobile_sensor_measures = MagicMock()
        mocked_database_gateway.update_last_acquisition = MagicMock()

        AddMobileMeasures(
            gateway=mocked_database_gateway,
            filter_ts=datetime.strptime("2021-08-10T23:58:00.000Z", "%Y-%m-%dT%H:%M:%S.000Z"),
            start_packet_id=12399,
            apiparam=APIParam(sensor_id=12, api_key="fakekey", api_id="fakeid", ch_name="main", last_acquisition=None)
        ).process(requests=mocked_request_builder)

        responses = mocked_database_gateway.insert_mobile_sensor_measures.call_args[1]['responses']
        self.assertEqual(len(responses), 1)
        resp = responses[0]

        expected_timestamp = "2021-08-10 23:59:00"
        expected_geom = "ST_GeomFromText('POINT(9.897 45.765)', 4326)"
        expected_measure_record = f"(12399, 66, 0.17, '{expected_timestamp}', {expected_geom})," \
                                  f"(12399, 48, 8, '{expected_timestamp}', {expected_geom})," \
                                  f"(12399, 94, 10, '{expected_timestamp}', {expected_geom})," \
                                  f"(12399, 2, 11, '{expected_timestamp}', {expected_geom})," \
                                  f"(12399, 4, 29, '{expected_timestamp}', {expected_geom})," \
                                  f"(12399, 12, 42, '{expected_timestamp}', {expected_geom})," \
                                  f"(12399, 39, 1004.68, '{expected_timestamp}', {expected_geom})"
        self.assertEqual(resp.measure_record, expected_measure_record)

        mocked_database_gateway.update_last_acquisition.assert_called_with(
            timestamp="2021-08-10 23:59:00",
            sensor_id=12,
            ch_name="main"
        )


if __name__ == '__main__':
    main()
