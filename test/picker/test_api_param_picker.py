#################################################
#
# @Author: davidecolombo
# @Date: ven, 29-10-2021, 08:26
# @Description: unit test script
#
#################################################

import unittest
from airquality.picker.api_param_picker import APIParamPicker


class TestAPIParamPicker(unittest.TestCase):

    def test_successfully_pick_parameters(self):
        test_api_param = {"p1": "v1", "p2": "v2"}
        test_param2pick = ["p1"]

        expected_output = {"p1": "v1"}
        actual_output = APIParamPicker.pick_param(api_param=test_api_param, param2pick=test_param2pick)
        self.assertEqual(actual_output, expected_output)

    def test_system_exit_when_empty_api_param_is_passed(self):
        test_api_param = {}
        test_param2pick = ["p1"]
        with self.assertRaises(SystemExit):
            APIParamPicker.pick_param(api_param=test_api_param, param2pick=test_param2pick)

    def test_output_api_param_when_param2pick_is_empty(self):
        test_api_param = {"p1": "v1", "p2": "v2"}
        test_param2pick = []

        expected_output = {"p1": "v1", "p2": "v2"}
        actual_output = APIParamPicker.pick_param(api_param=test_api_param, param2pick=test_param2pick)
        self.assertEqual(actual_output, expected_output)


if __name__ == '__main__':
    unittest.main()
