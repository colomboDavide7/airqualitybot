######################################################
#
# Author: Davide Colombo
# Date: 31/12/21 16:24
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import os
from unittest import TestCase, main
from unittest.mock import patch, MagicMock
from airquality.environment import Environment


def _fake_environ_personalities():
    return {
        'valid_personalities': 'p1,p2,p3'
    }


def _fake_environ_program_usage():
    tmp = _fake_environ_personalities()
    tmp.update({'program_usage_msg': "python(version) -m airquality [{pers}]"})
    return tmp


def _fake_environ_database_credentials():
    return {
        'dbname': "fakedbname",
        'host': "fakehost",
        'port': "fakeport",
        'user': "fakeuser",
        'password': "fakepassword",
    }


def _fake_environ_url_template():
    return {
        'p1_url': 'url_template_of_p1',
        'p2_url': 'url_template_of_p2',
        'p3_url': 'url_template_of_p3',
    }


def _fake_environ_resource_directory():
    return {
        'resource_dir': 'fakeroot',
        'p1_dir': 'fakep1dir',
        'p1_data_dir': 'fakep1datadir'
    }


def _fake_environ_logging_directory():
    return {
        "logging_dir": "fake_logging_dir"
    }


class TestEnvironment(TestCase):

# =========== TEST METHODS
    def test_get_valid_personalities(self):
        with patch.dict(os.environ, _fake_environ_personalities()):
            self.assertEqual(
                Environment().valid_personalities,
                ('p1', 'p2', 'p3')
            )

    def test_get_program_usage_msg(self):
        with patch.dict(os.environ, _fake_environ_program_usage()):
            self.assertEqual(
                Environment().program_usage_msg,
                "USAGE: python(version) -m airquality [p1 | p2 | p3]"
            )

    def test_get_database_credentials(self):
        with patch.dict(os.environ, _fake_environ_database_credentials()):
            env = Environment()
            self.assertEqual(env.dbname, "fakedbname")
            self.assertEqual(env.dbuser, "fakeuser")
            self.assertEqual(env.dbpwd, "fakepassword")
            self.assertEqual(env.dbhost, "fakehost")
            self.assertEqual(env.dbport, "fakeport")

    def test_get_url_from_personality(self):
        with patch.dict(os.environ, _fake_environ_url_template()):
            self.assertEqual(
                Environment().url_template(personality="p1"),
                "url_template_of_p1"
            )

    def test_input_dir_of(self):
        with patch.dict(os.environ, _fake_environ_resource_directory()):
            self.assertEqual(
                Environment().input_dir_of(personality="p1"),
                "fakeroot/fakep1dir/fakep1datadir"
            )

    def test_raise_missing_environ_property_error_when_key_error_is_raised(self):
        with patch.dict(os.environ, _fake_environ_personalities()):
            with self.assertRaises(KeyError):
                Environment().url_template('p4')

    @patch('airquality.environment.os.path')
    @patch('airquality.environment.os')
    def test_logging_dir_of(self, mocked_os, mocked_path):
        mocked_os.mkdir = MagicMock()
        mocked_path.exists.return_value = False
        mocked_os.environ = _fake_environ_logging_directory()
        self.assertEqual(
            Environment().logging_dir_of("fake_personality"),
            "fake_logging_dir/fake_personality"
        )
        mocked_os.mkdir.assert_called_with(
            path='fake_logging_dir/fake_personality',
            mode=0o600
        )


if __name__ == '__main__':
    main()
