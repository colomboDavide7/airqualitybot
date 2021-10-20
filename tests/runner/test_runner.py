#################################################
#
# @Author: davidecolombo
# @Date: lun, 18-10-2021, 12:49
# @Description: The unit test file for the 'airquality/runner.py' script
#
#################################################
import unittest
from airquality.runner import parse_sys_argv


class TestRunner(unittest.TestCase):
    """Class for testing the behaviour of the airquality.runner.py module."""

    def test_parse_sys_argv(self):
        """Check the correct parsing of sys argv parameters"""

        test_args = ['-d', '--ciao', 'usr', "ignored", "another_ignored"]
        expected_output = {"debug": True, "username": "usr"}
        actual_output = parse_sys_argv(test_args)
        self.assertEqual(actual_output, expected_output)

        test_args = ['-d', '--log', 'usr']
        expected_output = {"debug": True, "logging": True, "username": "usr"}
        actual_output = parse_sys_argv(test_args)
        self.assertEqual(actual_output, expected_output)

        test_args = ["usr"]
        expected_output = {"username": "usr"}
        actual_output = parse_sys_argv(test_args)
        self.assertEqual(actual_output, expected_output)

    def test_exit_on_help(self):
        """Test whether the python interpreter exits when '-h' or
        '--help' is the first argument.

        Even with missing 'username' argument but with help option
        it executes correctly.
        """

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
