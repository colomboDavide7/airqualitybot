######################################################
#
# Author: Davide Colombo
# Date: 30/12/21 08:56
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List
from datetime import datetime
from unittest import TestCase, main
from unittest.mock import MagicMock
from airquality.request_validator import AddFixedSensorRequestValidator, AddMobileMeasureRequestValidator
from airquality.request import AddFixedSensorRequest, Channel, Geolocation, AddMobileMeasureRequest


class TestRequestValidator(TestCase):

    @property
    def get_test_last_acquisition(self):
        return datetime.strptime("2021-10-11 09:44:00", "%Y-%m-%d %H:%M:%S")

    @property
    def get_test_geolocation(self):
        return Geolocation(latitude=11, longitude=-9)

    @property
    def get_test_channels(self):
        return [Channel(api_key="k", api_id="i", channel_name="n", last_acquisition=self.get_test_last_acquisition)]

    def get_test_add_fixed_sensor_request(self, names: List[str]):
        requests = []
        for name in names:
            requests.append(AddFixedSensorRequest(
                type="faketype", name=name, channels=self.get_test_channels, geolocation=self.get_test_geolocation
            ))
        return requests

    ##################################### test_validate_add_purpleair_sensor_request #####################################
    def test_validate_add_purpleair_sensor_request(self):
        mocked_request_builder = MagicMock()
        names = ['fakename1', 'fakename2']
        mocked_request_builder.__iter__.return_value = self.get_test_add_fixed_sensor_request(names=names)

        test_existing_names = {"fakename2", }

        valid_requests = AddFixedSensorRequestValidator(request=mocked_request_builder, existing_names=test_existing_names)
        self.assertEqual(len(valid_requests), 1)
        req = valid_requests[0]
        self.assertEqual(req.name, "fakename1")
        self.assertEqual(req.type, "faketype")

        with self.assertRaises(IndexError):
            print(valid_requests[1])

    @property
    def get_test_mobile_measures(self):
        return [(66, 0.17), (48, 8), (94, 10), (2, 11), (4, 29), (12, 42), (39, 1004.68)]

    def get_test_mobile_measure_request(self, timestamps: List[datetime]):
        requests = []
        for ts in timestamps:
            requests.append(AddMobileMeasureRequest(
                measures=self.get_test_mobile_measures, timestamp=ts, geolocation=self.get_test_geolocation)
            )
        return requests

    ##################################### test_validate_add_mobile_measure_request #####################################
    def test_validate_add_mobile_measure_request(self):
        mocked_request_builder = MagicMock()
        timestamps = [
            datetime.strptime("2021-08-10T23:59:00.000Z", "%Y-%m-%dT%H:%M:%S.000Z"),
            datetime.strptime("2021-08-11T00:00:00.000Z", "%Y-%m-%dT%H:%M:%S.000Z")
        ]
        mocked_request_builder.__iter__.return_value = self.get_test_mobile_measure_request(timestamps=timestamps)

        test_filter_ts = datetime.strptime("2021-08-10T23:59:00.000Z", "%Y-%m-%dT%H:%M:%S.000Z")
        valid_requests = AddMobileMeasureRequestValidator(request=mocked_request_builder, filter_ts=test_filter_ts)

        self.assertEqual(len(valid_requests), 1)
        req = valid_requests[0]
        self.assertEqual(req.timestamp, datetime.strptime("2021-08-11T00:00:00.000Z", "%Y-%m-%dT%H:%M:%S.000Z"))


if __name__ == '__main__':
    main()
