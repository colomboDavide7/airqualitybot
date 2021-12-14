######################################################
#
# Author: Davide Colombo
# Date: 27/11/21 17:39
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.filter.nameflt as flt
import airquality.api.resp.purpleair as purpresp


# ------------------------------- TestNameFilter ------------------------------- #
class TestNameFilter(unittest.TestCase):

    def setUp(self) -> None:
        self.test_responses = [
            purpresp.PurpleairAPIRespType(item={'name': 'n1', 'sensor_index': 'idx1'}),
            purpresp.PurpleairAPIRespType(item={'name': 'n2', 'sensor_index': 'idx2'}),
            purpresp.PurpleairAPIRespType(item={'name': 'n3', 'sensor_index': 'idx3'})
        ]

    def test_successfully_filter_names(self):
        test_database_names = ['n2 (idx2)']
        resp_filter = flt.NameFilter(names=test_database_names)
        actual = resp_filter.filter(all_resp=self.test_responses)
        self.assertEqual(len(actual), 2)
        self.assertEqual(actual[0].sensor_name(), "n1 (idx1)")
        self.assertEqual(actual[1].sensor_name(), "n3 (idx3)")

    def test_empty_filtered_list(self):
        test_database_names = ['n1 (idx1)', 'n2 (idx2)', 'n3 (idx3)']
        resp_filter = flt.NameFilter(names=test_database_names)
        actual = resp_filter.filter(all_resp=self.test_responses)
        self.assertEqual(len(actual), 0)


if __name__ == '__main__':
    unittest.main()
