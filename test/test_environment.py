######################################################
#
# Author: Davide Colombo
# Date: 31/12/21 16:24
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import os
from unittest.mock import patch
from unittest import TestCase, main
from airquality.environment import Environment


class TestEnvironment(TestCase):

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

    def test_raise_ValueError_when_invalid_personality_is_passed(self):
        with patch.dict(os.environ, self.get_test_environ):
            with self.assertRaises(ValueError):
                Environment(personality="fakepers")

    def test_get_valid_personalities(self):
        with patch.dict(os.environ, self.get_test_environ):
            actual = Environment(personality="p2").valid_personalities
            self.assertEqual(actual, ('p1', 'p2', 'p3'))

    def test_get_program_usage_msg(self):
        with patch.dict(os.environ, self.get_test_environ):
            actual = Environment(personality="p1").program_usage_msg
            self.assertEqual(actual, "python(version) -m airquality [p1 | p2 | p3]")

    def test_get_database_credentials(self):
        with patch.dict(os.environ, self.get_test_environ):
            env = Environment(personality="p3")
            self.assertEqual(env.dbname, "fakedbname")
            self.assertEqual(env.user, "fakeuser")
            self.assertEqual(env.password, "fakepassword")
            self.assertEqual(env.host, "fakehost")
            self.assertEqual(env.port, "fakeport")

    def test_get_url_from_personality(self):
        with patch.dict(os.environ, self.get_test_environ):
            actual = Environment(personality="p1").url_template
            self.assertEqual(actual, "url_template_of_p1")


if __name__ == '__main__':
    main()
