######################################################
#
# Author: Davide Colombo
# Date: 28/11/21 17:44
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.runner as runner


class TestRunner(unittest.TestCase):

    def test_successfully_get_commandline_arguments(self):
        test_args = ["init", "purpleair"]
        actual_command_name, actual_sensor_type = runner.get_commandline_arguments(test_args)
        self.assertEqual(actual_command_name, "init")
        self.assertEqual(actual_sensor_type, "purpleair")

    def test_exit_on_missing_arguments(self):
        with self.assertRaises(SystemExit):
            runner.get_commandline_arguments([])

    def test_exit_on_wrong_number_of_arguments(self):
        with self.assertRaises(SystemExit):
            runner.get_commandline_arguments(["a", "b", "c"])

        with self.assertRaises(SystemExit):
            runner.get_commandline_arguments(["a"])

    def test_exit_on_invalid_command_name(self):
        test_args = ["bad_command_name", "purpleair"]
        with self.assertRaises(SystemExit):
            runner.get_commandline_arguments(test_args)

    def test_exit_on_invalid_sensor_type(self):
        test_args = ["update", "bad type"]
        with self.assertRaises(SystemExit):
            runner.get_commandline_arguments(test_args)


if __name__ == '__main__':
    unittest.main()
