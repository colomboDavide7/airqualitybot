######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 14/11/21 19:59
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.filter.filter as filt
import airquality.database.util.datatype.timestamp as ts
import airquality.database.util.postgis.geom as geom
import airquality.adapter.config as c


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
        test_timestamp_before = {c.TIMEST: {c.CLS: ts.AtmotubeTimestamp, c.KW: {'timestamp': '2021-11-11T08:43:45.000Z'}}}
        actual_output = self.timest_filter.filter(sensor_data=test_timestamp_before)
        self.assertFalse(actual_output)

    def test_true_when_atmotube_data_is_after_filter_timestamp(self):
        test_timestamp_after = {c.TIMEST: {c.CLS: ts.AtmotubeTimestamp, c.KW: {'timestamp': '2021-11-11T08:45:45.000Z'}}}
        actual_output = self.timest_filter.filter(sensor_data=test_timestamp_after)
        self.assertTrue(actual_output)

    def test_false_when_thingspeak_data_is_before_filter_timestamp(self):
        test_timestamp_before = {c.TIMEST: {c.CLS: ts.ThingspeakTimestamp, c.KW: {'timestamp': '2021-11-11T08:43:45Z'}}}
        actual_output = self.timest_filter.filter(sensor_data=test_timestamp_before)
        self.assertFalse(actual_output)

    def test_true_when_thingspeak_data_is_after_filter_timestamp(self):
        test_timestamp_before = {c.TIMEST: {c.CLS: ts.ThingspeakTimestamp, c.KW: {'timestamp': '2021-11-11T08:45:45Z'}}}
        actual_output = self.timest_filter.filter(sensor_data=test_timestamp_before)
        self.assertTrue(actual_output)

    def test_system_exit_when_missing_filter_ts_dependency(self):
        packet_filter = filt.TimestampFilter()
        with self.assertRaises(SystemExit):
            packet_filter.filter(sensor_data={})

    ################################ NAME FILTER ################################
    def test_false_when_purpleair_sensor_name_is_within_database_sensors(self):
        test_name = {c.SENS_NAME: 'n1 (idx1)'}
        actual_output = self.name_filter.filter(test_name)
        self.assertFalse(actual_output)

    def test_true_when_purpleair_sensor_name_is_not_within_database_sensors(self):
        test_name = {c.SENS_NAME: 'n3 (idx3)'}
        actual_output = self.name_filter.filter(test_name)
        self.assertTrue(actual_output)

    ################################ GEO FILTER ################################
    def test_false_when_geo_filter_is_applied_to_inactive_sensor(self):
        test_data = {c.SENS_NAME: 'n3 (idx3)', c.SENS_GEOM: {c.CLS: geom.PointBuilder, c.KW: {'lat': '45', 'lng': '9'}}}
        actual_output = self.geo_filter.filter(sensor_data=test_data)
        self.assertFalse(actual_output)

    def test_false_when_geo_filter_is_applied_to_active_sensor_with_same_location(self):
        test_data = {c.SENS_NAME: 'n1 (idx1)', c.SENS_GEOM: {c.CLS: geom.PointBuilder, c.KW: {'lat': '45.1232', 'lng': '8.7876'}}}
        actual_output = self.geo_filter.filter(sensor_data=test_data)
        self.assertFalse(actual_output)

    def test_true_when_geo_filter_is_applied_to_active_sensor_with_new_location(self):
        test_data = {c.SENS_NAME: 'n1 (idx1)', c.SENS_GEOM: {c.CLS: geom.PointBuilder, c.KW: {'lat': '46', 'lng': '7'}}}
        actual_output = self.geo_filter.filter(sensor_data=test_data)
        self.assertTrue(actual_output)

    def test_empty_list_when_database_active_location_is_empty(self):
        test_data = {c.SENS_NAME: 'n1 (idx1)', c.SENS_GEOM: {c.CLS: geom.PointBuilder, c.KW: {'lat': '45', 'lng': '9'}}}
        geo_filter = filt.GeoFilter(database_active_locations={})
        actual_output = geo_filter.filter(sensor_data=test_data)
        self.assertFalse(actual_output)

    def test_exit_on_missing_geom_key_in_sensor_data(self):
        test_data = {c.SENS_NAME: 'n1 (idx1)'}
        geo_filter = filt.GeoFilter(database_active_locations={'n1 (idx1)': 'POINT(8.7876 45.1232)'})
        with self.assertRaises(SystemExit):
            geo_filter.filter(sensor_data=test_data)

    def test_exit_on_empty_geom_dictionary(self):
        test_data = {c.SENS_NAME: 'n1 (idx1)', 'geom': {}}
        geo_filter = filt.GeoFilter(database_active_locations={'n1 (idx1)': 'POINT(8.7876 45.1232)'})
        with self.assertRaises(SystemExit):
            geo_filter.filter(sensor_data=test_data)

    def test_exit_on_missing_class_or_kwargs_items_in_geom_dictionary(self):
        test_data = {c.SENS_NAME: 'n1 (idx1)', c.SENS_GEOM: {c.CLS: geom.PointBuilder, 'other': 1}}
        geo_filter = filt.GeoFilter(database_active_locations={'n1 (idx1)': 'POINT(8.7876 45.1232)'})
        with self.assertRaises(SystemExit):
            geo_filter.filter(sensor_data=test_data)


if __name__ == '__main__':
    unittest.main()
