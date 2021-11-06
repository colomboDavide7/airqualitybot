#################################################
#
# @Author: davidecolombo
# @Date: lun, 25-10-2021, 12:35
# @Description: unit test script
#
#################################################

# import unittest
# from airquality.plain.plain_api_packet import PlainAPIPacketPurpleair
# from airquality.constants.shared_constants import EMPTY_LIST


# class TestIdentifierPacketFilter(unittest.TestCase):
#
#     def test_successfully_filter_purpleair_packets(self):
#         """This method tests the correct behaviour of the purpleair filter class."""
#
#         test_packets = [PlainAPIPacketPurpleair({"name": "n1", "sensor_index": "idx1"}),
#                         PlainAPIPacketPurpleair({"name": "n2", "sensor_index": "idx2"}),
#                         PlainAPIPacketPurpleair({"name": "n3", "sensor_index": "idx3"})]
#
#         test_filter_list = ["n1 (idx1)"]
#         expected_output = [PlainAPIPacketPurpleair({"name": "n2", "sensor_index": "idx2"}),
#                            PlainAPIPacketPurpleair({"name": "n3", "sensor_index": "idx3"})]
#         filter_ = IdentifierPacketFilterFactory.create_identifier_filter(bot_personality="purpleair")
#         actual_output = filter_.filter_packets(containers=test_packets, identifiers=test_filter_list)
#         self.assertEqual(actual_output, expected_output)
#
#     def test_purpleair_filter_with_empty_filter_list(self):
#         """This method tests the behaviour of the purpleair filter method with 'filter_list' argument equal to
#         'EMPTY_LIST'."""
#
#         test_packets = [PlainAPIPacketPurpleair({"name": "n1", "sensor_index": "idx1"}),
#                         PlainAPIPacketPurpleair({"name": "n2", "sensor_index": "idx2"}),
#                         PlainAPIPacketPurpleair({"name": "n3", "sensor_index": "idx3"})]
#
#         test_filter_list = []
#         expected_output = [PlainAPIPacketPurpleair({"name": "n1", "sensor_index": "idx1"}),
#                            PlainAPIPacketPurpleair({"name": "n2", "sensor_index": "idx2"}),
#                            PlainAPIPacketPurpleair({"name": "n3", "sensor_index": "idx3"})]
#         filter_ = IdentifierPacketFilterFactory.create_identifier_filter(bot_personality="purpleair")
#         actual_output = filter_.filter_packets(containers=test_packets, identifiers=test_filter_list)
#         self.assertEqual(actual_output, expected_output)
#
#     def test_purpleair_filter_with_empty_packets(self):
#         """This method tests the return value of 'EMPTY_LIST' an empty list of packets is passed as argument."""
#
#         test_packets = EMPTY_LIST
#         test_filter_list = ["something1", "something2"]
#         expected_output = EMPTY_LIST
#         filter_ = IdentifierPacketFilterFactory.create_identifier_filter(bot_personality="purpleair")
#         actual_output = filter_.filter_packets(containers=test_packets, identifiers=test_filter_list)
#         self.assertEqual(actual_output, expected_output)
#
#
# if __name__ == '__main__':
#     unittest.main()
