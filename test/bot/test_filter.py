######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 14/11/21 19:59
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.bot.util.filter as filt
import airquality.database.util.datatype.timestamp as ts


class TestFilter(unittest.TestCase):

    def setUp(self) -> None:
        self.atmotube_ts_cls = ts.AtmotubeTimestamp
        self.thingspeak_ts_cls = ts.ThingspeakTimestamp
        self.filter_ts = ts.SQLTimestamp('2021-11-11 08:44:00')
        self.purpleair_names = ['n1 (idx1)', 'n2 (idx2)']

    def test_filter_atmotube_packets(self):
        test_packets = [{'timestamp': '2021-11-11T08:43:45.000Z'},
                        {'timestamp': '2021-11-11T08:45:45.000Z'}]
        packet_filter = filt.DateFilter(timest_cls=self.atmotube_ts_cls)
        packet_filter.set_filter_ts(self.filter_ts)
        actual_output = packet_filter.filter(test_packets)
        expected_output = [{'timestamp': '2021-11-11T08:45:45.000Z'}]
        self.assertEqual(actual_output, expected_output)

    def test_filter_thingspeak_packets(self):
        test_packets = [{'timestamp': '2021-11-11T08:43:45Z'},
                        {'timestamp': '2021-11-11T08:45:45Z'}]
        packet_filter = filt.DateFilter(timest_cls=self.thingspeak_ts_cls)
        packet_filter.set_filter_ts(self.filter_ts)
        actual_output = packet_filter.filter(test_packets)
        expected_output = [{'timestamp': '2021-11-11T08:45:45Z'}]
        self.assertEqual(actual_output, expected_output)

    def test_system_exit_when_missing_filter_ts_dependency(self):
        test_packets = []
        packet_filter = filt.DateFilter(timest_cls=self.thingspeak_ts_cls)
        with self.assertRaises(SystemExit):
            packet_filter.filter(test_packets)

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


if __name__ == '__main__':
    unittest.main()
