######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 06/11/21 11:12
# Description: INSERT HERE THE DESCRIPTION
#
######################################################

import unittest
from airquality.adapter.container_adapter import ContainerAdapterFactory, ContainerAdapterPurpleair


class TestContainerAdapter(unittest.TestCase):

    def test_successfully_adapt_purpleair_packets(self):
        test_packets = []
        expected_output = []

        fact = ContainerAdapterFactory(container_adapter_class=ContainerAdapterPurpleair)
        container_adapter = fact.make_container_adapter(packets=test_packets)
        actual_output = container_adapter.adapt_packets()
        self.assertEqual(actual_output, expected_output)


if __name__ == '__main__':
    unittest.main()
