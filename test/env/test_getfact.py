######################################################
#
# Author: Davide Colombo
# Date: 14/12/21 19:51
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.env.getfact as module


class TestEnvironment(unittest.TestCase):

    def test_system_exit_on_bad_arguments_combination(self):
        with self.assertRaises(SystemExit):
            module.get_env_fact(path_to_env="", command="init", target="atmotube")
        with self.assertRaises(SystemExit):
            module.get_env_fact(path_to_env="", command="init", target="thingspeak")
        with self.assertRaises(SystemExit):
            module.get_env_fact(path_to_env="", command="update", target="atmotube")
        with self.assertRaises(SystemExit):
            module.get_env_fact(path_to_env="", command="update", target="thingspeak")
        with self.assertRaises(SystemExit):
            module.get_env_fact(path_to_env="", command="fetch", target="purpleair")
        with self.assertRaises(SystemExit):
            module.get_env_fact(path_to_env="", command="fetch", target="geonames")


if __name__ == '__main__':
    unittest.main()
