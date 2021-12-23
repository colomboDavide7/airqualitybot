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
from airquality.program_handler import ProgramHandler, Option


class TestProgramHandler(TestCase):

    def setUp(self) -> None:
        self.test_environ = {
            "valid_personalities": "p1,p2,p3,p4",
            "program_usage_msg": "python(version) -m airquality [{pers}] [{opt}]",
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
                with ProgramHandler() as ph:
                    expected_options = [Option(pers='p3', short_name='-a', long_name='--all')]
                    self.assertEqual(ph.options, expected_options)
                    self.assertEqual(ph.valid_personalities, ['p1', 'p2', 'p3', 'p4'])
                    self.assertEqual(ph.personality, "p1")
                    expected_usage_msg = "python(version) -m airquality [p1|p2|p3|p4] [-a,--all]"
                    self.assertEqual(ph.program_usage_message, expected_usage_msg)
                    self.assertEqual(ph.dbname, "test_db")
                    self.assertEqual(ph.port, "test_port")
                    self.assertEqual(ph.host, "test_host")
                    self.assertEqual(ph.user, "test_user")
                    self.assertEqual(ph.password, "test_password")

    def test_ValueError_when_arguments_length_is_less_than_one(self):
        test_argv = ["program_name"]

        with patch.object(sys, 'argv', test_argv):
            with self.assertRaises(ValueError):
                ProgramHandler()

    def test_KeyError_when_handler_is_used_without_context_manager(self):
        test_argv = ["program_name", "p4"]

        with patch.object(sys, 'argv', test_argv):
            with self.assertRaises(KeyError):
                handler = ProgramHandler()
                handler.personality


if __name__ == '__main__':
    main()
