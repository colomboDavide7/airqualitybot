######################################################
#
# Author: Davide Colombo
# Date: 29/12/21 18:09
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from unittest import TestCase, main
from airquality.datamodel.response import AddFixedSensorResponse, AddMobileMeasureResponse, AddStationMeasuresResponse


class TestResponseModel(TestCase):

    def test_add_fixed_sensor_response_model(self):

        record = AddFixedSensorResponse(
            sensor_record="fake_sensor_record", apiparam_record="fake_apiparam_record", geolocation_record="fake_geo_record"
        )
        self.assertEqual(record.sensor_record, "fake_sensor_record")
        self.assertEqual(record.apiparam_record, "fake_apiparam_record")
        self.assertEqual(record.geolocation_record, "fake_geo_record")

    def test_add_mobile_measure_response_model(self):

        record = AddMobileMeasureResponse(
            measure_record="fake_measure_record"
        )
        self.assertEqual(record.measure_record, "fake_measure_record")

    def test_add_station_measures_response_model(self):
        response = AddStationMeasuresResponse(
            measure_record="fake_measure_records"
        )
        self.assertEqual(response.measure_record, "fake_measure_records")


if __name__ == '__main__':
    main()
