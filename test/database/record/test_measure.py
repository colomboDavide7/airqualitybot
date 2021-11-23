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
import airquality.adapter.config as adapt_const
import airquality.database.util.datatype.config as time_conf
import airquality.database.util.postgis.config as geom_conf


class TestMeasurementRecord(unittest.TestCase):

    def setUp(self) -> None:
        self.time_rec = t.TimeRecord()
        self.location_rec = loc.LocationRecord()
        self.mobile_rec = rec.MobileMeasureRecord(time_rec=self.time_rec, location_rec=self.location_rec)
        self.station_rec = rec.StationMeasureRecord(self.time_rec)

    ################################ STATION MEASUREMENT RECORD ################################
    def test_successfully_build_station_record(self):
        test_data = {adapt_const.REC_ID: 99,
                     adapt_const.SENS_PARAM: [{adapt_const.PAR_ID: 1, adapt_const.PAR_VAL: 55}],
                     adapt_const.TIMEST: {adapt_const.CLS: ts.ThingspeakTimestamp,
                                          adapt_const.KW: {time_conf.TIMEST_INIT_TIMESTAMP: '2018-10-11T09:44:00Z'}}}
        actual_output = self.station_rec.record(test_data, sensor_id=144)
        expected_output = "(99, 1, 144, '55', '2018-10-11 09:44:00')"
        self.assertEqual(actual_output, expected_output)

    def test_exit_when_missing_sensor_id(self):
        test_data = {adapt_const.REC_ID: 99,
                     adapt_const.SENS_PARAM: [{adapt_const.PAR_ID: 1, adapt_const.PAR_VAL: 55}],
                     adapt_const.TIMEST: {adapt_const.CLS: ts.ThingspeakTimestamp,
                                          adapt_const.KW: {time_conf.TIMEST_INIT_TIMESTAMP: '2018-10-11T09:44:00Z'}}}
        with self.assertRaises(SystemExit):
            self.station_rec.record(test_data)

    ################################ MOBILE MEASUREMENT RECORD ################################
    def test_successfully_build_mobile_record(self):
        test_data = {adapt_const.REC_ID: 99,
                     adapt_const.SENS_PARAM: [{adapt_const.PAR_ID: 1, adapt_const.PAR_VAL: 55}],
                     adapt_const.TIMEST: {adapt_const.CLS: ts.AtmotubeTimestamp,
                                          adapt_const.KW: {time_conf.TIMEST_INIT_TIMESTAMP: '2018-10-11T09:44:00.000Z'}},
                     adapt_const.SENS_GEOM: {adapt_const.CLS: geom.PostgisPoint,
                                             adapt_const.KW: {geom_conf.POINT_INIT_LAT_NAME: '45',
                                                              geom_conf.POINT_INIT_LNG_NAME: '9'}}}
        actual_output = self.mobile_rec.record(sensor_data=test_data)
        expected_output = "(99, 1, '55', '2018-10-11 09:44:00', ST_GeomFromText('POINT(9 45)', 26918))"
        self.assertEqual(actual_output, expected_output)

    def test_exit_on_missing_record_id_mobile_record(self):
        test_missing_record_id = {adapt_const.SENS_PARAM: [{adapt_const.PAR_ID: 1, adapt_const.PAR_VAL: 55}],
                                  adapt_const.TIMEST: {adapt_const.CLS: ts.AtmotubeTimestamp,
                                                       adapt_const.KW: {time_conf.TIMEST_INIT_TIMESTAMP: '2018-10-11T09:44:00.000Z'}},
                                  adapt_const.SENS_GEOM: {adapt_const.CLS: geom.PostgisPoint,
                                                          adapt_const.KW: {geom_conf.POINT_INIT_LAT_NAME: '45',
                                                                           geom_conf.POINT_INIT_LNG_NAME: '9'}}}
        with self.assertRaises(SystemExit):
            self.mobile_rec.record(test_missing_record_id)

    def test_exit_on_missing_param(self):
        test_missing_param = {adapt_const.REC_ID: 99,
                              adapt_const.TIMEST: {adapt_const.CLS: ts.AtmotubeTimestamp,
                                                   adapt_const.KW: {time_conf.TIMEST_INIT_TIMESTAMP: '2018-10-11T09:44:00.000Z'}},
                              adapt_const.SENS_GEOM: {adapt_const.CLS: geom.PostgisPoint,
                                                      adapt_const.KW: {geom_conf.POINT_INIT_LAT_NAME: '45',
                                                                       geom_conf.POINT_INIT_LNG_NAME: '9'}}}
        with self.assertRaises(SystemExit):
            rec._exit_on_missing_measure_param_data(test_missing_param)

    def test_exit_on_empty_param_list(self):
        test_missing_param_val = {adapt_const.REC_ID: 99,
                                  adapt_const.SENS_PARAM: [],
                                  adapt_const.TIMEST: {adapt_const.CLS: ts.AtmotubeTimestamp,
                                                       adapt_const.KW: {time_conf.TIMEST_INIT_TIMESTAMP: '2018-10-11T09:44:00.000Z'}},
                                  adapt_const.SENS_GEOM: {adapt_const.CLS: geom.PostgisPoint,
                                                          adapt_const.KW: {geom_conf.POINT_INIT_LAT_NAME: '45',
                                                                           geom_conf.POINT_INIT_LNG_NAME: '9'}}}
        with self.assertRaises(SystemExit):
            rec._exit_on_missing_measure_param_data(test_missing_param_val)

    def test_exit_on_missing_param_id_or_param_value(self):
        test_missing_param_id = {adapt_const.REC_ID: 99, adapt_const.SENS_PARAM: [{'val': 55}],
                                 adapt_const.TIMEST: {adapt_const.CLS: ts.AtmotubeTimestamp,
                                                      adapt_const.KW: {time_conf.TIMEST_INIT_TIMESTAMP: '2018-10-11T09:44:00.000Z'}},
                                 adapt_const.SENS_GEOM: {adapt_const.CLS: geom.PostgisPoint,
                                                         adapt_const.KW: {geom_conf.POINT_INIT_LAT_NAME: '45',
                                                                          geom_conf.POINT_INIT_LNG_NAME: '9'}}}
        with self.assertRaises(SystemExit):
            self.mobile_rec.record(test_missing_param_id)


if __name__ == '__main__':
    unittest.main()
