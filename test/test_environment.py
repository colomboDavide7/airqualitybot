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
from airquality.environment import Environment, MissingEnvironPropertyError


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
            'p3_url': 'url_template_of_p3',
            'resource_dir': 'fakeroot',
            'p1_dir': 'fakep1dir',
            'p1_data_dir': 'fakep1datadir'
        }

    def test_get_valid_personalities(self):
        with patch.dict(os.environ, self.get_test_environ):
            env = Environment()
            actual = env.valid_personalities
            self.assertEqual(actual, ('p1', 'p2', 'p3'))

    def test_get_program_usage_msg(self):
        with patch.dict(os.environ, self.get_test_environ):
            actual = Environment().program_usage_msg
            self.assertEqual(actual, "USAGE: python(version) -m airquality [p1 | p2 | p3]")

    def test_get_database_credentials(self):
        with patch.dict(os.environ, self.get_test_environ):
            env = Environment()
            self.assertEqual(env.dbname, "fakedbname")
            self.assertEqual(env.dbuser, "fakeuser")
            self.assertEqual(env.dbpwd, "fakepassword")
            self.assertEqual(env.dbhost, "fakehost")
            self.assertEqual(env.dbport, "fakeport")

    def test_get_url_from_personality(self):
        with patch.dict(os.environ, self.get_test_environ):
            env = Environment()
            actual = env.url_template(personality="p1")
            self.assertEqual(actual, "url_template_of_p1")

    def test_input_dir_of(self):
        with patch.dict(os.environ, self.get_test_environ):
            env = Environment()
            actual = env.input_dir_of(personality="p1")
            self.assertEqual(actual, "fakeroot/fakep1dir/fakep1datadir")

    def test_EnvironmentError_when_KeyError_is_raised(self):
        with patch.dict(os.environ, self.get_test_environ):
            with self.assertRaises(MissingEnvironPropertyError):
                env = Environment()
                env.url_template('p4')


if __name__ == '__main__':
    main()
