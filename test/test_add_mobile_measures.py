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
from airquality.datamodel import AtmotubeDatamodel
from airquality.add_mobile_measures import AddMobileMeasures


class TestAddMobileMeasuresUsecase(TestCase):

    @property
    def get_test_atmotube_datamodel(self):
        return AtmotubeDatamodel(
            time="2021-08-10T23:59:00.000Z",
            voc=0.17,
            pm1=8,
            pm25=10,
            pm10=11,
            t=29,
            h=42,
            p=1004.68,
            coords={'lat': 45.876, 'lon': 9.145}
        )

    @property
    def get_test_code2id(self):
        return {'voc': 66, 'pm1': 48, 'pm25': 94, 'pm10': 2, 't': 4, 'h': 12, 'p': 39}

    def test_add_mobile_measures(self):
        mocked_datamodel = MagicMock()
        mocked_datamodel.__len__.return_value = 1
        mocked_datamodel.__iter__.return_value = [self.get_test_atmotube_datamodel]

        mocked_database_gateway = MagicMock()
        mocked_database_gateway.insert_mobile_sensor_measures = MagicMock()
        mocked_database_gateway.update_last_acquisition = MagicMock()

        AddMobileMeasures(
            output_gateway=mocked_database_gateway,
            filter_ts=datetime.strptime("2021-08-10T23:58:00.000Z", "%Y-%m-%dT%H:%M:%S.000Z"),
            code2id=self.get_test_code2id,
            start_packet_id=12399,
            sensor_id=12,
            ch_name="main"
        ).process(datamodels=mocked_datamodel)

        responses = mocked_database_gateway.insert_mobile_sensor_measures.call_args[1]['responses']
        self.assertEqual(len(responses), 1)
        resp = responses[0]

        expected_timestamp = "2021-08-10 23:59:00"
        expected_geom = "ST_GeomFromText('POINT(9.145 45.876)', 26918)"
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
