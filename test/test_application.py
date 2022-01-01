######################################################
#
# Author: Davide Colombo
# Date: 31/12/21 19:03
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from airquality.application import Application, WrongUsageError
from airquality.environment import Environment
from unittest import TestCase, main
from unittest.mock import patch
import sys
import os


class TestApplication(TestCase):

    @property
    def get_test_environ(self):
        return {
            'valid_personalities': 'p1,p2,p3',
            'program_usage_msg': "python(version) -m airquality [{pers}]",
            'dbname': "fakedbname",
            'host': "fakehost",
            'port': "fakeport",
            'user': "fakeuser",
            'password': "fakepassword",
            'p1_url': 'url_template_of_p1',
            'p2_url': 'url_template_of_p2',
            'p3_url': 'url_template_of_p3'
        }

    def test_create_WrongUsageError(self):
        err = WrongUsageError(cause="some cause")
        self.assertEqual(err.cause, "some cause")
        self.assertEqual(repr(err), "WrongUsageError(cause=some cause)")

    def test_WrongUsageError_on_missing_personality(self):
        test_args = ['program_name']
        with patch.object(sys, 'argv', test_args):
            with patch.dict(os.environ, self.get_test_environ):
                with Application(env=Environment()) as runner:
                    with self.assertRaises(WrongUsageError):
                        runner.main()

    def test_WrongUsageError_on_invalid_personality(self):
        test_args = ['program_name', 'bad_personality']
        with patch.object(sys, 'argv', test_args):
            with patch.dict(os.environ, self.get_test_environ):
                with Application(env=Environment()) as runner:
                    with self.assertRaises(WrongUsageError):
                        runner.main()


if __name__ == '__main__':
    main()
