######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 13/11/21 15:56
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
from typing import Dict, Any
import airquality.to_delete.config as adapt_const
import database.ext.config as geom_conf
import database.dtype.config as time_conf
import api2db.measure as adapt
import airquality.database.op.sel.sensor as sel_type
import types.postgis as geom
import types.timestamp as ts
import airquality.api.config as extr_const


############################## ATMOTUBE MOCK #############################
class AtmotubeTypeSelectWrapperMock(sel_type.TypeSelectWrapper):

    def get_max_record_id(self):
        return 99

    def get_measure_param(self) -> Dict[str, Any]:
        return {'voc': 1, 'pm1': 2, 'pm25': 3, 'pm10': 4, 't': 5, 'h': 6, 'p': 7}


############################## THINGSPEAK MOCK #############################
class ThingspeakTypeSelectWrapperMock(sel_type.TypeSelectWrapper):

    def get_max_record_id(self):
        return 99

    def get_measure_param(self) -> Dict[str, Any]:
        return {'f1': 9, 'f2': 10}


############################## TEST CLASS #############################
class TestMeasureAdapter(unittest.TestCase):

    def setUp(self) -> None:
        self.atmotube_adapter = adapt.AtmotubeMeasureAdapter(
            sel_type=AtmotubeTypeSelectWrapperMock(conn=None, query_builder=None, sensor_type=None),
            geom_cls=geom.PostgisPoint,
            timest_cls=ts.AtmotubeTimestamp
        )
        self.thingspeak_adapter = adapt.ThingspeakMeasureAdapter(
            sel_type=ThingspeakTypeSelectWrapperMock(conn=None, query_builder=None, sensor_type=None),
            timest_cls=ts.ThingspeakTimestamp
        )

    ############################## TEST ATMOTUBE MEASURE ADAPTER #############################
    def test_successfully_reshape_atmotube_measurements(self):
        test_packet = {'voc': 'val1', 'pm1': 'val2', 'pm25': 'val3', 'pm10': 'val4', 't': 'val5', 'h': 'val6',
                       'p': 'val7', 'time': '2021-10-11T01:33:44.000Z'}
        expected_output = {adapt_const.REC_ID: 99,
                           adapt_const.SENS_PARAM: [{adapt_const.PAR_ID: 1, adapt_const.PAR_VAL: 'val1'},
                                                    {adapt_const.PAR_ID: 2, adapt_const.PAR_VAL: 'val2'},
                                                    {adapt_const.PAR_ID: 3, adapt_const.PAR_VAL: 'val3'},
                                                    {adapt_const.PAR_ID: 4, adapt_const.PAR_VAL: 'val4'},
                                                    {adapt_const.PAR_ID: 5, adapt_const.PAR_VAL: 'val5'},
                                                    {adapt_const.PAR_ID: 6, adapt_const.PAR_VAL: 'val6'},
                                                    {adapt_const.PAR_ID: 7, adapt_const.PAR_VAL: 'val7'}],
                           adapt_const.TIMEST: {adapt_const.CLS: ts.AtmotubeTimestamp,
                                                adapt_const.KW: {time_conf.TIMEST_INIT_TIMESTAMP: '2021-10-11T01:33:44.000Z'}},
                           adapt_const.SENS_GEOM: {adapt_const.CLS: geom.NullGeometry,
                                                   adapt_const.KW: {}}
                           }
        actual_output = self.atmotube_adapter.reshape(test_packet)
        self.assertEqual(actual_output, expected_output)

    def test_successfully_reshape_atmotube_measurements_with_coords(self):
        test_packet = {'voc': 'val1', 'pm1': 'val2', 'pm25': 'val3', 'pm10': 'val4', 't': 'val5', 'h': 'val6',
                       'p': 'val7', 'time': '2021-10-11T01:33:44.000Z', 'coords': {'lat': 'lat_val', 'lon': 'lon_val'}}
        expected_output = {adapt_const.REC_ID: 99,
                           adapt_const.SENS_PARAM: [{adapt_const.PAR_ID: 1, adapt_const.PAR_VAL: 'val1'},
                                                    {adapt_const.PAR_ID: 2, adapt_const.PAR_VAL: 'val2'},
                                                    {adapt_const.PAR_ID: 3, adapt_const.PAR_VAL: 'val3'},
                                                    {adapt_const.PAR_ID: 4, adapt_const.PAR_VAL: 'val4'},
                                                    {adapt_const.PAR_ID: 5, adapt_const.PAR_VAL: 'val5'},
                                                    {adapt_const.PAR_ID: 6, adapt_const.PAR_VAL: 'val6'},
                                                    {adapt_const.PAR_ID: 7, adapt_const.PAR_VAL: 'val7'}],
                           adapt_const.TIMEST: {adapt_const.CLS: ts.AtmotubeTimestamp,
                                                adapt_const.KW: {time_conf.TIMEST_INIT_TIMESTAMP: '2021-10-11T01:33:44.000Z'}},
                           adapt_const.SENS_GEOM: {adapt_const.CLS: geom.PostgisPoint,
                                                   adapt_const.KW: {geom_conf.POINT_INIT_LAT_NAME: 'lat_val',
                                                                    geom_conf.POINT_INIT_LNG_NAME: 'lon_val'}}
                           }
        actual_output = self.atmotube_adapter.reshape(test_packet)
        self.assertEqual(actual_output, expected_output)

    def test_none_value_on_missing_param(self):
        # Test output when 't', 'h' and 'p' are missing
        test_packet = {'voc': 'val1', 'pm1': 'val2', 'pm25': 'val3', 'pm10': 'val4', 'time': '2021-10-11T01:33:44.000Z'}
        expected_output = {adapt_const.REC_ID: 99,
                           adapt_const.SENS_PARAM: [{adapt_const.PAR_ID: 1, adapt_const.PAR_VAL: 'val1'},
                                                    {adapt_const.PAR_ID: 2, adapt_const.PAR_VAL: 'val2'},
                                                    {adapt_const.PAR_ID: 3, adapt_const.PAR_VAL: 'val3'},
                                                    {adapt_const.PAR_ID: 4, adapt_const.PAR_VAL: 'val4'},
                                                    {adapt_const.PAR_ID: 5, adapt_const.PAR_VAL: None},
                                                    {adapt_const.PAR_ID: 6, adapt_const.PAR_VAL: None},
                                                    {adapt_const.PAR_ID: 7, adapt_const.PAR_VAL: None}],
                           adapt_const.TIMEST: {adapt_const.CLS: ts.AtmotubeTimestamp,
                                                adapt_const.KW: {time_conf.TIMEST_INIT_TIMESTAMP: '2021-10-11T01:33:44.000Z'}},
                           adapt_const.SENS_GEOM: {adapt_const.CLS: geom.NullGeometry,
                                                   adapt_const.KW: {}}
                           }
        actual_output = self.atmotube_adapter.reshape(test_packet)
        self.assertEqual(actual_output, expected_output)

    def test_exit_on_bad_atmotube_coords_item(self):
        test_bad_coords = {'voc': 'val1', 'pm1': 'val2', 'pm25': 'val3', 'pm10': 'val4', 't': 'val5', 'h': 'val6',
                           'p': 'val7', 'coords': {}}
        with self.assertRaises(SystemExit):
            self.atmotube_adapter.reshape(test_bad_coords)

    def test_exit_on_missing_atmotube_time_item(self):
        test_missing_time = {'voc': 'val1', 'pm1': 'val2', 'pm25': 'val3', 'pm10': 'val4', 't': 'val5', 'h': 'val6',
                             'p': 'val7'}
        with self.assertRaises(SystemExit):
            self.atmotube_adapter.reshape(test_missing_time)

    ############################## TEST THINGSPEAK MEASURE ADAPTER #############################
    def test_successfully_adapt_thingspeak_data(self):
        test_packet = {'created_at': '2021-10-11T01:33:44Z',
                       extr_const.CHANNEL_FIELDS: [{extr_const.FIELD_NAME: 'f1', extr_const.FIELD_VALUE: 'val1'},
                                                   {extr_const.FIELD_NAME: 'f2', extr_const.FIELD_VALUE: 'val2'}]}

        expected_output = {adapt_const.REC_ID: 99,
                           adapt_const.SENS_PARAM: [{adapt_const.PAR_ID: 9, adapt_const.PAR_VAL: 'val1'},
                                                    {adapt_const.PAR_ID: 10, adapt_const.PAR_VAL: 'val2'}],
                           adapt_const.TIMEST: {adapt_const.CLS: ts.ThingspeakTimestamp,
                                                adapt_const.KW: {time_conf.TIMEST_INIT_TIMESTAMP: '2021-10-11T01:33:44Z'}}}
        actual_output = self.thingspeak_adapter.reshape(test_packet)
        self.assertEqual(actual_output, expected_output)

    def test_none_value_when_measure_is_missing(self):
        test_packet = {'created_at': '2021-10-11T01:33:44Z',
                       extr_const.CHANNEL_FIELDS: [{extr_const.FIELD_NAME: 'f1', extr_const.FIELD_VALUE: None},
                                                   {extr_const.FIELD_NAME: 'f2', extr_const.FIELD_VALUE: 'val2'}]}
        expected_output = {adapt_const.REC_ID: 99,
                           adapt_const.SENS_PARAM: [{adapt_const.PAR_ID: 9, adapt_const.PAR_VAL: None},
                                                    {adapt_const.PAR_ID: 10, adapt_const.PAR_VAL: 'val2'}],
                           adapt_const.TIMEST: {adapt_const.CLS: ts.ThingspeakTimestamp,
                                                adapt_const.KW: {time_conf.TIMEST_INIT_TIMESTAMP: '2021-10-11T01:33:44Z'}}}
        actual_output = self.thingspeak_adapter.reshape(test_packet)
        self.assertEqual(actual_output, expected_output)

    def test_exit_on_missing_value_item_within_fields(self):
        test_packet = {'created_at': '2021-10-11T01:33:44Z',
                       extr_const.CHANNEL_FIELDS: [{extr_const.FIELD_NAME: 'f1', 'bad_key': 'val1'},
                                                   {extr_const.FIELD_NAME: 'f2', 'bad_key': 'val2'}]}
        with self.assertRaises(SystemExit):
            self.thingspeak_adapter.reshape(test_packet)

    def test_exit_on_missing_name_item_within_fields(self):
        test_packet = {'created_at': '2021-10-11T01:33:44Z',
                       extr_const.CHANNEL_FIELDS: [{'bad_key': 'f1', extr_const.FIELD_VALUE: 'val1'},
                                                   {'bad_key': 'f2', extr_const.FIELD_VALUE: 'val2'}]}
        with self.assertRaises(SystemExit):
            self.thingspeak_adapter.reshape(test_packet)

    def test_exit_on_missing_fields_item(self):
        test_packet = {'created_at': '2021-10-11T01:33:44Z'}
        with self.assertRaises(SystemExit):
            self.thingspeak_adapter.reshape(test_packet)

    def test_exit_on_missing_created_at_item(self):
        test_packet = {extr_const.CHANNEL_FIELDS: [{extr_const.FIELD_NAME: 'f1', extr_const.FIELD_VALUE: None},
                                                   {extr_const.FIELD_NAME: 'f2', extr_const.FIELD_VALUE: 'val2'}]}
        with self.assertRaises(SystemExit):
            self.thingspeak_adapter.reshape(test_packet)


if __name__ == '__main__':
    unittest.main()
