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
from airquality.datamodel.apidata import ThingspeakAPIData
from airquality.usecase.add_station_measures import AddStationMeasures


class TestAddStationMeasuresUsecase(TestCase):

    @property
    def get_test_thingspeak_apidata_model(self):
        return ThingspeakAPIData(
            created_at="2021-12-20T11:18:40Z",
            field1="20.50",
            field2="35.53",
            field3="37.43",
            field6="55",
            field7="60"
        )

    @property
    def get_test_filter_timestamp(self):
        return datetime.strptime("2021-12-09T15:52:34Z", "%Y-%m-%dT%H:%M:%SZ")

    @property
    def get_test_field_map(self):
        return {'field1': 'p1', 'field2': 'p2', 'field3': 'p3', 'field6': 'p6', 'field7': 'p7'}

    @property
    def get_test_code2id(self):
        return {'p1': 12, 'p2': 13, 'p3': 14, 'p6': 15, 'p7': 16}

    def test_add_station_measures(self):
        mocked_thingspeak_datamodel = MagicMock()
        mocked_thingspeak_datamodel.__len__.return_value = 1
        mocked_thingspeak_datamodel.__iter__.return_value = [self.get_test_thingspeak_apidata_model]

        mocked_gateway = MagicMock()
        mocked_gateway.insert_station_measures = MagicMock()
        mocked_gateway.update_last_acquisition = MagicMock()

        AddStationMeasures(
            output_gateway=mocked_gateway,
            filter_ts=self.get_test_filter_timestamp,
            code2id=self.get_test_code2id,
            field_map=self.get_test_field_map,
            start_packet_id=140,
            sensor_id=99,
            ch_name="fakename"
        ).process(datamodels=mocked_thingspeak_datamodel)

        responses = mocked_gateway.insert_station_measures.call_args[1]['responses']
        self.assertEqual(len(responses), 1)

        resp = responses[0]
        expected_measure_record = "(140, 99, 12, 20.5, '2021-12-20 11:18:40'),(140, 99, 13, 35.53, '2021-12-20 11:18:40')," \
                                  "(140, 99, 14, 37.43, '2021-12-20 11:18:40'),(140, 99, 15, 55.0, '2021-12-20 11:18:40')," \
                                  "(140, 99, 16, 60.0, '2021-12-20 11:18:40')"
        self.assertEqual(resp.measure_record, expected_measure_record)


if __name__ == '__main__':
    main()
