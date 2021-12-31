######################################################
#
# Author: Davide Colombo
# Date: 31/12/21 19:03
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from airquality.runner import Runner, WrongUsageError
from airquality.environment import Environment
from unittest import TestCase, main
from unittest.mock import patch
import sys


class TestRunner(TestCase):

    def test_create_WrongUsageError(self):
        err = WrongUsageError(cause="some cause")
        self.assertEqual(err.cause, "some cause")
        self.assertEqual(repr(err), "WrongUsageError(cause=some cause)")

    def test_WrongUsageError_on_missing_personality(self):
        test_args = ['program_name']
        with patch.object(sys, 'argv', test_args):
            with Runner(env=Environment()) as runner:
                with self.assertRaises(WrongUsageError):
                    runner.main()

    def test_WrongUsageError_on_invalid_personality(self):
        test_args = ['program_name', 'bad_personality']
        with patch.object(sys, 'argv', test_args):
            with Runner(env=Environment()) as runner:
                with self.assertRaises(WrongUsageError):
                    runner.main()


if __name__ == '__main__':
    main()
