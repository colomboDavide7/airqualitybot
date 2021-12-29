######################################################
#
# Author: Davide Colombo
# Date: 29/12/21 18:09
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from unittest import TestCase, main
from airquality.sqlrecord import FixedSensorSQLRecord, MobileMeasureSQLRecord


class TestSQLRecordModel(TestCase):

    def test_fixed_sensor_sql_record(self):

        record = FixedSensorSQLRecord(
            sensor_record="fake_sensor_record", apiparam_record="fake_apiparam_record", geolocation_record="fake_geo_record"
        )

        self.assertEqual(record.sensor_record, "fake_sensor_record")
        self.assertEqual(record.apiparam_record, "fake_apiparam_record")
        self.assertEqual(record.geolocation_record, "fake_geo_record")

    def test_mobile_measure_sql_record(self):

        record = MobileMeasureSQLRecord(
            measure_record="fake_measure_record"
        )

        self.assertEqual(record.measure_record, "fake_measure_record")


if __name__ == '__main__':
    main()
