######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 06/11/21 10:44
# Description: INSERT HERE THE DESCRIPTION
#
######################################################

import unittest
from airquality.filter.container_filter import ContainerIdentifierFilter


class TestContainerFilter(unittest.TestCase):

    def test_false_when_identifier_is_into_filter_list(self):
        test_filter_list = ['n1', 'n2', 'n3']
        container_filter = ContainerIdentifierFilter(filter_list=test_filter_list)
        actual_output = container_filter.filter_container(to_filter='n1')
        self.assertFalse(actual_output)

    def test_true_when_identifier_is_not_into_filter_list(self):
        test_filter_list = ['n1', 'n2', 'n3']
        container_filter = ContainerIdentifierFilter(filter_list=test_filter_list)
        actual_output = container_filter.filter_container(to_filter='n4')
        self.assertTrue(actual_output)

    def test_true_when_filter_list_is_empty(self):
        test_filter_list = []
        container_filter = ContainerIdentifierFilter(filter_list=test_filter_list)
        actual_output = container_filter.filter_container(to_filter='n4')
        self.assertTrue(actual_output)


if __name__ == '__main__':
    unittest.main()
