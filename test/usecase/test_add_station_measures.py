######################################################
#
# Author: Davide Colombo
# Date: 01/01/22 16:30
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from datetime import datetime
from unittest import TestCase, main
from unittest.mock import MagicMock
from airquality.datamodel.apiparam import APIParam
from airquality.datamodel.request import AddSensorMeasuresRequest
from airquality.usecase.add_station_measures import AddStationMeasures


class TestAddStationMeasuresUsecase(TestCase):

    @property
    def get_test_thingspeak_request(self):
        return AddSensorMeasuresRequest(
            timestamp=datetime.strptime("2021-12-20T11:18:40Z", "%Y-%m-%dT%H:%M:%SZ"),
            measures=[(12, 20.50), (13, 35.53), (14, 37.43), (15, 55.0), (16, 60.0)]
        )

    @property
    def get_test_filter_timestamp(self):
        return datetime.strptime("2021-12-09T15:52:34Z", "%Y-%m-%dT%H:%M:%SZ")

    def test_add_station_measures(self):
        mocked_request_builder = MagicMock()
        mocked_request_builder.__len__.return_value = 1
        mocked_request_builder.__iter__.return_value = [self.get_test_thingspeak_request]

        mocked_gateway = MagicMock()
        mocked_gateway.insert_station_measures = MagicMock()
        mocked_gateway.update_last_acquisition = MagicMock()

        AddStationMeasures(
            output_gateway=mocked_gateway,
            filter_ts=self.get_test_filter_timestamp,
            start_packet_id=140,
            apiparam=APIParam(sensor_id=99, api_key="fakekey", api_id="fakeid", ch_name="fakename", last_acquisition=None)
        ).process(requests=mocked_request_builder)

        responses = mocked_gateway.insert_station_measures.call_args[1]['responses']
        self.assertEqual(len(responses), 1)

        resp = responses[0]
        expected_measure_record = "(140, 99, 12, 20.5, '2021-12-20 11:18:40'),(140, 99, 13, 35.53, '2021-12-20 11:18:40')," \
                                  "(140, 99, 14, 37.43, '2021-12-20 11:18:40'),(140, 99, 15, 55.0, '2021-12-20 11:18:40')," \
                                  "(140, 99, 16, 60.0, '2021-12-20 11:18:40')"
        self.assertEqual(resp.measure_record, expected_measure_record)


if __name__ == '__main__':
    main()
