######################################################
#
# Author: Davide Colombo
# Date: 23/12/21 11:26
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import sys
import os
from unittest import TestCase, main
from unittest.mock import patch
from airquality.env import Environment, Option, HelpException


class TestProgramHandler(TestCase):

    def setUp(self) -> None:
        self.test_environ = {
            "valid_personalities": "p1,p2,p3,p4",
            "program_usage_msg": "python(version) -m airquality [{pers}]",
            "p3_opt": "-a,--all",
            "database": "test_db",
            "host": "test_host",
            "port": "test_port",
            "user": "test_user",
            "password": "test_password"
        }

    def test_program_handler_correct_behaviour(self):
        test_argv = ['prog_name', 'p1']

        with patch.object(sys, 'argv', test_argv):
            with patch.dict(os.environ, self.test_environ):
                with Environment() as ph:
                    expected_options = [Option(pers='p1', short_name='', long_name=''),
                                        Option(pers='p2', short_name='', long_name=''),
                                        Option(pers='p3', short_name='-a', long_name='--all'),
                                        Option(pers='p4', short_name='', long_name='')]
                    self.assertEqual(ph.valid_options, expected_options)
                    self.assertEqual(ph.valid_personalities, ['p1', 'p2', 'p3', 'p4'])
                    self.assertEqual(ph.personality, "p1")
                    expected_usage_msg = "python(version) -m airquality [p1 [] | p2 [] | p3 [-a,--all] | p4 []]"
                    self.assertEqual(ph.program_usage_message, expected_usage_msg)
                    self.assertEqual(ph.dbname, "test_db")
                    self.assertEqual(ph.port, "test_port")
                    self.assertEqual(ph.host, "test_host")
                    self.assertEqual(ph.user, "test_user")
                    self.assertEqual(ph.password, "test_password")
                    self.assertEqual(ph.options, [])

    def test_extract_options(self):
        test_argv = ['prog_name', 'p3', '-a', '--bad_option']

        with patch.object(sys, 'argv', test_argv):
            with patch.dict(os.environ, self.test_environ):
                with Environment() as ph:
                    inserted_options = ph.options
                    expected = [Option(pers="p3", short_name="-a", long_name="--all")]
                    self.assertEqual(inserted_options, expected)

    def test_ValueError_when_arguments_length_is_less_than_one(self):
        test_argv = ["program_name"]

        with patch.object(sys, 'argv', test_argv):
            with self.assertRaises(ValueError):
                Environment()

    def test_KeyError_when_handler_is_used_without_context_manager(self):
        test_argv = ["program_name", "p4"]

        with patch.object(sys, 'argv', test_argv):
            with self.assertRaises(KeyError):
                handler = Environment()
                print(handler.personality)

    def test_help_exception_when_personality_is_help(self):
        test_argv = ['program_name', 'help']

        with patch.object(sys, 'argv', test_argv):
            with patch.dict(os.environ, self.test_environ):
                with Environment() as ph:
                    with self.assertRaises(HelpException):
                        print(ph.personality)


if __name__ == '__main__':
    main()
