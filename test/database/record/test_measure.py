######################################################
#
# Author: Davide Colombo
# Date: 16/11/21 12:40
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.database.util.record.record as rec
import airquality.database.util.record.time as t
import airquality.database.util.datatype.timestamp as ts
import airquality.database.util.record.location as loc
import airquality.database.util.postgis.geom as geom
import airquality.adapter.config as c


class TestMeasurementRecord(unittest.TestCase):

    def setUp(self) -> None:
        self.time_rec = t.TimeRecord()
        self.location_rec = loc.LocationRecord()
        self.mobile_rec = rec.MobileMeasureRecord(time_rec=self.time_rec, location_rec=self.location_rec)
        self.station_rec = rec.StationMeasureRecord(self.time_rec)

    ################################ STATION MEASUREMENT RECORD ################################
    def test_successfully_build_station_record(self):
        test_data = {c.REC_ID: 99,
                     c.SENS_PARAM: [{c.PAR_ID: 1, c.PAR_VAL: 55}],
                     c.TIMEST: {c.CLS: ts.ThingspeakTimestamp, c.KW: {'timestamp': '2018-10-11T09:44:00Z'}}}
        actual_output = self.station_rec.record(test_data, sensor_id=144)
        expected_output = "(99, 1, 144, '55', '2018-10-11 09:44:00')"
        self.assertEqual(actual_output, expected_output)

    def test_exit_when_missing_sensor_id(self):
        test_data = {c.REC_ID: 99,
                     c.SENS_PARAM: [{c.PAR_ID: 1, c.PAR_VAL: 55}],
                     c.TIMEST: {c.CLS: ts.ThingspeakTimestamp, c.KW: {'timestamp': '2018-10-11T09:44:00Z'}}}
        with self.assertRaises(SystemExit):
            self.station_rec.record(test_data)

    ################################ MOBILE MEASUREMENT RECORD ################################
    def test_successfully_build_mobile_record(self):
        test_data = {c.REC_ID: 99,
                     c.SENS_PARAM: [{c.PAR_ID: 1, c.PAR_VAL: 55}],
                     c.TIMEST: {c.CLS: ts.AtmotubeTimestamp, c.KW: {'timestamp': '2018-10-11T09:44:00.000Z'}},
                     c.SENS_GEOM: {c.CLS: geom.PointBuilder, c.KW: {'lat': '45', 'lng': '9'}}}
        actual_output = self.mobile_rec.record(sensor_data=test_data)
        expected_output = "(99, 1, '55', '2018-10-11 09:44:00', ST_GeomFromText('POINT(9 45)', 26918))"
        self.assertEqual(actual_output, expected_output)

    def test_exit_on_missing_record_id_mobile_record(self):
        test_missing_record_id = {c.SENS_PARAM: [{c.PAR_ID: 1, c.PAR_VAL: 55}],
                                  c.TIMEST: {c.CLS: ts.AtmotubeTimestamp, c.KW: {'timestamp': '2018-10-11T09:44:00.000Z'}},
                                  c.SENS_GEOM: {c.CLS: geom.PointBuilder, c.KW: {'lat': '45', 'lng': '9'}}}
        with self.assertRaises(SystemExit):
            self.mobile_rec.record(test_missing_record_id)

    def test_exit_on_missing_param(self):
        test_missing_param = {c.REC_ID: 99,
                              c.TIMEST: {c.CLS: ts.AtmotubeTimestamp, c.KW: {'timestamp': '2018-10-11T09:44:00.000Z'}},
                              c.SENS_GEOM: {'class': geom.PointBuilder, 'kwargs': {'lat': '45', 'lng': '9'}}}
        with self.assertRaises(SystemExit):
            rec._exit_on_missing_measure_param_data(test_missing_param)

    def test_exit_on_empty_param_list(self):
        test_missing_param_val = {c.REC_ID: 99,
                                  c.SENS_PARAM: [],
                                  c.TIMEST: {c.CLS: ts.AtmotubeTimestamp, c.KW: {'timestamp': '2018-10-11T09:44:00.000Z'}},
                                  c.SENS_GEOM: {c.CLS: geom.PointBuilder, c.KW: {'lat': '45', 'lng': '9'}}}
        with self.assertRaises(SystemExit):
            rec._exit_on_missing_measure_param_data(test_missing_param_val)

    def test_exit_on_missing_param_id_or_param_value(self):
        test_missing_param_id = {c.REC_ID: 99, c.SENS_PARAM: [{'val': 55}],
                                 c.TIMEST: {c.CLS: ts.AtmotubeTimestamp, c.KW: {'timestamp': '2018-10-11T09:44:00.000Z'}},
                                 c.SENS_GEOM: {c.CLS: geom.PointBuilder, c.KW: {'lat': '45', 'lng': '9'}}}
        with self.assertRaises(SystemExit):
            self.mobile_rec.record(test_missing_param_id)


if __name__ == '__main__':
    unittest.main()
