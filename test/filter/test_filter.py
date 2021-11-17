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

class TestFilter(unittest.TestCase):

    def setUp(self) -> None:
        self.atmotube_ts_cls = ts.AtmotubeTimestamp
        self.thingspeak_ts_cls = ts.ThingspeakTimestamp
        self.filter_ts = ts.SQLTimestamp('2021-11-11 08:44:00')
        self.purpleair_names = ['n1 (idx1)', 'n2 (idx2)']
        self.postgis_point = geom.PointBuilder()

    ################################ TIMESTAMP FILTER ################################
    def test_filter_atmotube_packets(self):
        test_packets = [{'timestamp': '2021-11-11T08:43:45.000Z'},
                        {'timestamp': '2021-11-11T08:45:45.000Z'}]
        packet_filter = filt.TimestampFilter(timestamp_class=self.atmotube_ts_cls)
        packet_filter.set_filter_ts(self.filter_ts)
        actual_output = packet_filter.filter(test_packets)
        expected_output = [{'timestamp': '2021-11-11T08:45:45.000Z'}]
        self.assertEqual(actual_output, expected_output)

    def test_filter_thingspeak_packets(self):
        test_packets = [{'timestamp': '2021-11-11T08:43:45Z'},
                        {'timestamp': '2021-11-11T08:45:45Z'}]
        packet_filter = filt.TimestampFilter(timestamp_class=self.thingspeak_ts_cls)
        packet_filter.set_filter_ts(self.filter_ts)
        actual_output = packet_filter.filter(test_packets)
        expected_output = [{'timestamp': '2021-11-11T08:45:45Z'}]
        self.assertEqual(actual_output, expected_output)

    def test_system_exit_when_missing_filter_ts_dependency(self):
        test_packets = []
        packet_filter = filt.TimestampFilter(timestamp_class=self.thingspeak_ts_cls)
        with self.assertRaises(SystemExit):
            packet_filter.filter(test_packets)

    ################################ NAME FILTER ################################
    def test_purpleair_name_filter(self):
        test_fetched_sensors = [{"name": 'n1 (idx1)'}, {"name": 'n2 (idx2)'}, {"name": 'n3 (idx3)'}]
        packet_filter = filt.NameFilter()
        packet_filter.set_name_to_filter(self.purpleair_names)
        actual_output = packet_filter.filter(test_fetched_sensors)
        expected_output = [{"name": 'n3 (idx3)'}]
        self.assertEqual(actual_output, expected_output)

    def test_system_exit_when_missing_database_sensor_external_dependency(self):
        test_fetched_sensors = [{"name": 'n1 (idx1)'}, {"name": 'n2 (idx2)'}, {"name": 'n3 (idx3)'}]
        packet_filter = filt.NameFilter()
        with self.assertRaises(SystemExit):
            packet_filter.filter(test_fetched_sensors)

    ################################ GEO FILTER ################################
    def test_geo_filter(self):
        test_data = [{'name': 'n1 (idx1)', 'lat': '45', 'lng': '9'}]
        geo_filter = filt.GeoFilter(postgis_builder=self.postgis_point)
        geo_filter.set_database_active_locations({'n1 (idx1)': 'POINT(8.7876 45.1232)'})
        actual_output = geo_filter.filter(sensor_data=test_data)
        expected_output = [{'name': 'n1 (idx1)', 'lat': '45', 'lng': '9'}]
        self.assertEqual(actual_output, expected_output)

    def test_exit_on_missing_geo_filter_database_sensor_names(self):
        test_data = [{'name': 'n1 (idx1)', 'lat': '45', 'lng': '9'}]
        geo_filter = filt.GeoFilter(postgis_builder=self.postgis_point)
        with self.assertRaises(SystemExit):
            geo_filter.filter(sensor_data=test_data)

    def test_empty_list_when_geolocation_is_the_same(self):
        test_data = [{'name': 'n1 (idx1)', 'lat': '45', 'lng': '9'}]
        geo_filter = filt.GeoFilter(postgis_builder=self.postgis_point)
        geo_filter.set_database_active_locations({'n1 (idx1)': 'POINT(9 45)'})
        actual_output = geo_filter.filter(sensor_data=test_data)
        expected_output = []
        self.assertEqual(actual_output, expected_output)


if __name__ == '__main__':
    unittest.main()
