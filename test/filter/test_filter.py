#################################################
#
# @Author: davidecolombo
# @Date: lun, 25-10-2021, 12:35
# @Description: unit test script
#
#################################################

import unittest
from airquality.filter.filter import APIPacketFilter
from airquality.constants.shared_constants import EMPTY_LIST, ATMOTUBE_TIME_PARAM


class TestFilter(unittest.TestCase):


    def test_successfully_filter_purpleair_packets(self):
        """This method tests the correct behaviour of the purple air filter class."""

        test_packets = [{"name": "n1", "sensor_index": "idx1"},
                        {"name": "n2", "sensor_index": "idx2"},
                        {"name": "n3", "sensor_index": "idx3"}]

        test_filter_list = ["n1 (idx1)"]
        expected_output = [{"name": "n2", "sensor_index": "idx2"},
                           {"name": "n3", "sensor_index": "idx3"}]
        actual_output = APIPacketFilter.filter_packet_by_sensor_name(packets = test_packets,
                                                                     filter_name_list = test_filter_list,
                                                                     identifier = "purpleair")
        self.assertEqual(actual_output, expected_output)


    def test_purpleair_filter_with_empty_filter_list(self):
        """This method tests the behaviour of the purpleair filter method with 'filter_list' argument equal to
        'EMPTY_LIST'."""

        test_packets = [{"name": "n1", "sensor_index": "idx1"},
                        {"name": "n2", "sensor_index": "idx2"},
                        {"name": "n3", "sensor_index": "idx3"}]

        test_filter_list = EMPTY_LIST
        expected_output = [{"name": "n1", "sensor_index": "idx1"},
                           {"name": "n2", "sensor_index": "idx2"},
                           {"name": "n3", "sensor_index": "idx3"}]
        actual_output = APIPacketFilter.filter_packet_by_sensor_name(packets = test_packets,
                                                                     filter_name_list = test_filter_list,
                                                                     identifier = "purpleair")
        self.assertEqual(actual_output, expected_output)


    def test_purpleair_filter_with_empty_packets(self):
        """This method tests the return value of 'EMPTY_LIST' an empty list of packets is passed as argument."""

        test_packets = EMPTY_LIST
        test_filter_list = ["something1", "something2"]
        expected_output = EMPTY_LIST
        actual_output = APIPacketFilter.filter_packet_by_sensor_name(packets = test_packets,
                                                                     filter_name_list = test_filter_list,
                                                                     identifier = "purpleair")
        self.assertEqual(actual_output, expected_output)



    # def test_successfully_filter_atmotube_packets(self):
    #     test_packets = [{ATMOTUBE_TIME_PARAM: "2021-10-11T09:44:00.000Z"},
    #                     {ATMOTUBE_TIME_PARAM: "2021-10-11T09:45:00.000Z"},
    #                     {ATMOTUBE_TIME_PARAM: "2021-10-11T09:46:00.000Z"}]
    #     test_sqltimestamp = "2021-10-11 09:45:00"
    #     expected_output = [{ATMOTUBE_TIME_PARAM: "2021-10-11T09:46:00.000Z"}]
    #     actual_output = APIPacketFilter.filter_packet_from_timestamp_on(packets = test_packets,
    #                                                                     sqltimestamp = test_sqltimestamp,
    #                                                                     identifier = "atmotube")
    #     self.assertEqual(actual_output, expected_output)



if __name__ == '__main__':
    unittest.main()
