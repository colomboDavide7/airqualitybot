#################################################
#
# @Author: davidecolombo
# @Date: lun, 18-10-2021, 12:49
# @Description: The unit test file for the 'airquality/runner.py' script
#
#################################################
import unittest
from airquality.runner import parse_sys_argv, check_username


class TestRunner(unittest.TestCase):
    """Class for testing the behaviour of the airquality.runner.py module."""

    def test_parse_sys_argv(self):
        """Check the correct parsing of sys argv parameters"""

        # TEST 1 - BOTH VALID AND INVALID ARGS
        test_args = ['ciao', '-d', 'line', '--log', '-h']
        expected_output = {"debug": True, "logging": True}
        actual_output = parse_sys_argv(test_args)
        self.assertEqual(actual_output, expected_output)

        # TEST 2 - ONLY INVALID ARGS
        test_args = ['ciao', 'line']
        expected_output = {}
        actual_output = parse_sys_argv(test_args)
        self.assertEqual(actual_output, expected_output)

        test_args = ['atmotube', 'purpleair']
        expected_output = {"username": "atmotube"}
        actual_output = parse_sys_argv(test_args)
        self.assertEqual(actual_output, expected_output)

    def test_SystemExit_check_username(self):
        """Test system exit if username is not provided or is invalid."""
        invalid_kwargs = {"debug": True, "logging": True}
        with self.assertRaises(SystemExit):
            check_username(invalid_kwargs)

    def test_exit_on_help(self):
        """Test whether the python interpreter exits when '-h' or
        '--help' is the first argument"""

        test_args = ["-h", "--debug", "--log", "ciao"]
        with self.assertRaises(SystemExit):
            parse_sys_argv(test_args)

        test_args = ["--help", "--debug", "--log", "ciao"]
        with self.assertRaises(SystemExit):
            parse_sys_argv(test_args)


################################ EXECUTABLE ################################
if __name__ == '__main__':
    unittest.main()
