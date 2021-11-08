######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 06/11/21 11:12
# Description: INSERT HERE THE DESCRIPTION
#
######################################################

import unittest
from airquality.adapter.universal_adapter import ContainerAdapterFactory, PurpleairUniversalAdapter


class TestContainerAdapter(unittest.TestCase):

    def setUp(self) -> None:
        self.purpleair_fact = ContainerAdapterFactory(container_adapter_class=PurpleairUniversalAdapter)

    def test_successfully_adapt_purpleair_packets(self):
        test_packet = {'name': 'n1', 'sensor_index': 'idx1', 'geometry': 'geom', 'timestamp': 'ts',
                       'primary_id_a': 'id1A', 'primary_id_b': 'id1B', 'primary_key_a': 'key1A', 'primary_key_b': 'key1B',
                       'secondary_id_a': 'id2A', 'secondary_id_b': 'id2B', 'secondary_key_a': 'key2A',
                       'secondary_key_b': 'key2B', 'primary_timestamp_a': 'null', 'primary_timestamp_b': 'null',
                       'secondary_timestamp_a': 'null', 'secondary_timestamp_b': 'null'}

        expected_output = {'name': 'n1 (idx1)', 'type': 'purpleair', 'timestamp': 'ts', 'geometry': 'geom',
                           'param_name': ['primary_id_a', 'primary_id_b', 'primary_key_a', 'primary_key_b',
                                          'secondary_id_a', 'secondary_id_b', 'secondary_key_a', 'secondary_key_b',
                                          'primary_timestamp_a', 'primary_timestamp_b', 'secondary_timestamp_a',
                                          'secondary_timestamp_b'],
                           'param_value': ['id1A', 'id1B', 'key1A', 'key1B', 'id2A', 'id2B', 'key2A', 'key2B',
                                           'null', 'null', 'null', 'null']}

        container_adapter = self.purpleair_fact.make_container_adapter()
        actual_output = container_adapter.adapt(api_param=test_packet)
        self.assertEqual(actual_output, expected_output)

    def test_system_exit_when_key_error_occur_purpleair_container_adapter(self):
        test_packet = {'name': 'n1', 'sensor_index': 'idx1',
                       'primary_id_a': 'id1A', 'primary_id_b': 'id1B', 'primary_key_a': 'key1A',
                       'secondary_id_a': 'id2A', 'secondary_id_b': 'id2B', 'secondary_key_a': 'key2A',
                       'secondary_timestamp_a': 'null', 'secondary_timestamp_b': 'null'}

        container_adapter = self.purpleair_fact.make_container_adapter()
        with self.assertRaises(SystemExit):
            container_adapter.adapt(api_param=test_packet)


if __name__ == '__main__':
    unittest.main()
