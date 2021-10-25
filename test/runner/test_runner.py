#################################################
#
# @Author: davidecolombo
# @Date: lun, 18-10-2021, 12:49
# @Description: unit test script
#
#################################################
import unittest
from fetch.runner import parse_sys_argv


class TestRunner(unittest.TestCase):


    def test_parse_sys_argv(self):
        """Test the correct parsing of sys argv parameters"""

        test_args = ['-d', '--ciao', 'atmotube', "ignored", "another_ignored", "1"]
        expected_output = {"debug": True, "personality": "atmotube", "api_address_number": "1"}
        actual_output = parse_sys_argv(test_args)
        self.assertEqual(actual_output, expected_output)

        test_args = ['-d', '--log', 'atmotube', '1']
        expected_output = {"debug": True, "logging": True, "personality": "atmotube", "api_address_number": "1"}
        actual_output = parse_sys_argv(test_args)
        self.assertEqual(actual_output, expected_output)

        test_args = ["atmotube", "2"]
        expected_output = {"personality": "atmotube", "api_address_number": "2"}
        actual_output = parse_sys_argv(test_args)
        self.assertEqual(actual_output, expected_output)

    def test_exit_on_help(self):
        """Test whether the python interpreter exits when '-h' or '--help' is the first argument."""

        test_args = ["-h", "--debug", "--log"]
        with self.assertRaises(SystemExit):
            parse_sys_argv(test_args)

        test_args = ["--help", "--debug", "--log", "usr"]
        with self.assertRaises(SystemExit):
            parse_sys_argv(test_args)

    def test_system_exit_missing_username(self):
        """Test SystemExit when username is not provided."""

        test_args = ['-d', '-l']
        with self.assertRaises(SystemExit):
            parse_sys_argv(test_args)



################################ EXECUTABLE ################################
if __name__ == '__main__':
    unittest.main()
