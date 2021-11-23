######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 14/11/21 19:59
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.filter.base as filt
import airquality.database.util.datatype.timestamp as ts
import airquality.database.util.postgis.geom as geom
import airquality.adapter.config as adapt_const
import airquality.database.util.datatype.config as time_conf
import airquality.database.util.postgis.config as geom_conf


class TestFilter(unittest.TestCase):

    def setUp(self) -> None:
        self.atmotube_ts_cls = ts.AtmotubeTimestamp
        self.thingspeak_ts_cls = ts.ThingspeakTimestamp
        self.timest_filter = filt.TimestampFilter()
        self.timest_filter.set_filter_ts(filter_ts=ts.SQLTimestamp('2021-11-11 08:44:00'))
        self.name_filter = filt.NameFilter(database_sensor_names=['n1 (idx1)', 'n2 (idx2)'])
        self.geo_filter = filt.GeoFilter(database_active_locations={'n1 (idx1)': 'POINT(8.7876 45.1232)'})

    ################################ TIMESTAMP FILTER ################################
    def test_false_when_atmotube_data_is_before_filter_timestamp(self):
        test_timestamp_before = {adapt_const.TIMEST: {adapt_const.CLS: ts.AtmotubeTimestamp,
                                                      adapt_const.KW: {time_conf.TIMEST_INIT_TIMESTAMP: '2021-11-11T08:43:45.000Z'}}}
        actual_output = self.timest_filter.filter(sensor_data=test_timestamp_before)
        self.assertFalse(actual_output)

    def test_true_when_atmotube_data_is_after_filter_timestamp(self):
        test_timestamp_after = {adapt_const.TIMEST: {adapt_const.CLS: ts.AtmotubeTimestamp,
                                                     adapt_const.KW: {time_conf.TIMEST_INIT_TIMESTAMP: '2021-11-11T08:45:45.000Z'}}}
        actual_output = self.timest_filter.filter(sensor_data=test_timestamp_after)
        self.assertTrue(actual_output)

    def test_false_when_thingspeak_data_is_before_filter_timestamp(self):
        test_timestamp_before = {adapt_const.TIMEST: {adapt_const.CLS: ts.ThingspeakTimestamp,
                                                      adapt_const.KW: {time_conf.TIMEST_INIT_TIMESTAMP: '2021-11-11T08:43:45Z'}}}
        actual_output = self.timest_filter.filter(sensor_data=test_timestamp_before)
        self.assertFalse(actual_output)

    def test_true_when_thingspeak_data_is_after_filter_timestamp(self):
        test_timestamp_before = {adapt_const.TIMEST: {adapt_const.CLS: ts.ThingspeakTimestamp,
                                                      adapt_const.KW: {time_conf.TIMEST_INIT_TIMESTAMP: '2021-11-11T08:45:45Z'}}}
        actual_output = self.timest_filter.filter(sensor_data=test_timestamp_before)
        self.assertTrue(actual_output)

    def test_system_exit_when_missing_filter_ts_dependency(self):
        packet_filter = filt.TimestampFilter()
        with self.assertRaises(SystemExit):
            packet_filter.filter(sensor_data={})

    ################################ NAME FILTER ################################
    def test_false_when_purpleair_sensor_name_is_within_database_sensors(self):
        test_name = {adapt_const.SENS_NAME: 'n1 (idx1)'}
        actual_output = self.name_filter.filter(test_name)
        self.assertFalse(actual_output)

    def test_true_when_purpleair_sensor_name_is_not_within_database_sensors(self):
        test_name = {adapt_const.SENS_NAME: 'n3 (idx3)'}
        actual_output = self.name_filter.filter(test_name)
        self.assertTrue(actual_output)

    ################################ GEO FILTER ################################
    def test_false_when_geo_filter_is_applied_to_inactive_sensor(self):
        test_data = {adapt_const.SENS_NAME: 'n3 (idx3)',
                     adapt_const.SENS_GEOM: {adapt_const.CLS: geom.PostgisPoint,
                                             adapt_const.KW: {geom_conf.POINT_INIT_LAT_NAME: '45',
                                                              geom_conf.POINT_INIT_LNG_NAME: '9'}}}
        actual_output = self.geo_filter.filter(sensor_data=test_data)
        self.assertFalse(actual_output)

    def test_false_when_geo_filter_is_applied_to_active_sensor_with_same_location(self):
        test_data = {adapt_const.SENS_NAME: 'n1 (idx1)',
                     adapt_const.SENS_GEOM: {adapt_const.CLS: geom.PostgisPoint,
                                             adapt_const.KW: {geom_conf.POINT_INIT_LAT_NAME: '45.1232',
                                                              geom_conf.POINT_INIT_LNG_NAME: '8.7876'}}}
        actual_output = self.geo_filter.filter(sensor_data=test_data)
        self.assertFalse(actual_output)

    def test_true_when_geo_filter_is_applied_to_active_sensor_with_new_location(self):
        test_data = {adapt_const.SENS_NAME: 'n1 (idx1)',
                     adapt_const.SENS_GEOM: {adapt_const.CLS: geom.PostgisPoint,
                                             adapt_const.KW: {geom_conf.POINT_INIT_LAT_NAME: '46',
                                                              geom_conf.POINT_INIT_LNG_NAME: '7'}}}
        actual_output = self.geo_filter.filter(sensor_data=test_data)
        self.assertTrue(actual_output)

    def test_empty_list_when_database_active_location_is_empty(self):
        test_data = {adapt_const.SENS_NAME: 'n1 (idx1)',
                     adapt_const.SENS_GEOM: {adapt_const.CLS: geom.PostgisPoint,
                                             adapt_const.KW: {geom_conf.POINT_INIT_LAT_NAME: '45',
                                                              geom_conf.POINT_INIT_LNG_NAME: '9'}}}
        geo_filter = filt.GeoFilter(database_active_locations={})
        actual_output = geo_filter.filter(sensor_data=test_data)
        self.assertFalse(actual_output)

    def test_exit_on_missing_geom_key_in_sensor_data(self):
        test_data = {adapt_const.SENS_NAME: 'n1 (idx1)'}
        geo_filter = filt.GeoFilter(database_active_locations={'n1 (idx1)': 'POINT(8.7876 45.1232)'})
        with self.assertRaises(SystemExit):
            geo_filter.filter(sensor_data=test_data)

    def test_exit_on_empty_geom_dictionary(self):
        test_data = {adapt_const.SENS_NAME: 'n1 (idx1)', 'geom': {}}
        geo_filter = filt.GeoFilter(database_active_locations={'n1 (idx1)': 'POINT(8.7876 45.1232)'})
        with self.assertRaises(SystemExit):
            geo_filter.filter(sensor_data=test_data)

    def test_exit_on_missing_class_or_kwargs_items_in_geom_dictionary(self):
        test_data = {adapt_const.SENS_NAME: 'n1 (idx1)', adapt_const.SENS_GEOM: {adapt_const.CLS: geom.PostgisPoint, 'other': 1}}
        geo_filter = filt.GeoFilter(database_active_locations={'n1 (idx1)': 'POINT(8.7876 45.1232)'})
        with self.assertRaises(SystemExit):
            geo_filter.filter(sensor_data=test_data)


if __name__ == '__main__':
    unittest.main()
