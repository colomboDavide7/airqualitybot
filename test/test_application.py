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


def _fake_environ():
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


class TestApplication(TestCase):

# =========== TEST METHODS
    def test_raise_wrong_usage_error_when_arg1_is_missing(self):
        program_args = ['program_name']
        with patch.object(sys, 'argv', program_args):
            with patch.dict(os.environ, _fake_environ()):
                with self.assertRaises(SystemExit):
                    with Application() as app:
                        with self.assertRaises(WrongUsageError):
                            app.main()
                    self.assertEqual(app._exit_code, 1)

    def test_raise_wrong_usage_error_when_arg1_is_invalid(self):
        program_args = ['program_name', 'bad_personality']
        with patch.object(sys, 'argv', program_args):
            with patch.dict(os.environ, _fake_environ()):
                with self.assertRaises(SystemExit):
                    with Application() as app:
                        with self.assertRaises(WrongUsageError):
                            app.main()
                    self.assertEqual(app._exit_code, 1)


if __name__ == '__main__':
    main()
