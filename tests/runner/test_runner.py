#################################################
#
# @Author: davidecolombo
# @Date: lun, 18-10-2021, 12:49
# @Description: The unit test file for the 'airquality/runner.py' script
#
#################################################
import os.path
import unittest

from airquality.runner import parse_sys_argv


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


    def test_exit_on_help(self):
        """Test whether the python interpreter exits when '-h' or
        '--help' is the first argument"""

        test_args = ["-h", "--debug", "--log", "ciao"]
        with self.assertRaises(SystemExit):
            parse_sys_argv(test_args)

        test_args = ["--help", "--debug", "--log", "ciao"]
        with self.assertRaises(SystemExit):
            parse_sys_argv(test_args)


    def test_get_resource_file_path(self):
        """Test insertion of the resource file path from the prompt."""

        with self.assertRaises(FileNotFoundError):
            TestRunner.__get_resource_path_mock("bad/path")

        with self.assertRaises(ValueError):
            TestRunner.__get_resource_path_mock(
                    "/Users/davidecolombo/Desktop/"
                    "airquality/airquality/runner.py")

        valid_path = "/Users/davidecolombo/Desktop/airquality/" \
                     "properties/resources.json"
        actual_output = TestRunner.__get_resource_path_mock(valid_path)
        self.assertEqual(actual_output, valid_path)

    @staticmethod
    def __get_resource_path_mock(path: str) -> str:
        """Mocking function for the 'runner.get_resource_file_path()'"""

        if not os.path.isfile(path):
            raise FileNotFoundError(f"path to file {path} is not valid.")

        if "properties/resources.json" not in path:
            raise ValueError(f"Path to file {path} is wrong.")
        return path


################################ EXECUTABLE ################################
if __name__ == '__main__':
    unittest.main()
