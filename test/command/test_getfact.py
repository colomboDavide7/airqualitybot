######################################################
#
# Author: Davide Colombo
# Date: 28/11/21 18:13
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.command.getfact as get
import airquality.command.init.fact as initfact
import airquality.command.update.fact as updtfact
import airquality.command.fetch.atmfact as atm
import airquality.command.fetch.thnkfact as thnk


class TestCommandFactory(unittest.TestCase):

    def test_successfully_get_purpleair_init_command_class(self):
        test_command_name = "init"
        test_sensor_type = "purpleair"
        actual_cls = get.get_command_factory_cls(command_name=test_command_name, sensor_type=test_sensor_type)
        expected_cls = initfact.PurpleairInitFactory
        self.assertEqual(actual_cls, expected_cls)

    def test_successfully_get_purpleair_update_command_class(self):
        test_command_name = "update"
        test_sensor_type = "purpleair"
        actual_cls = get.get_command_factory_cls(command_name=test_command_name, sensor_type=test_sensor_type)
        expected_cls = updtfact.PurpleairUpdateFactory
        self.assertEqual(actual_cls, expected_cls)

    def test_successfully_get_atmotube_fetch_command_class(self):
        test_command_name = "fetch"
        test_sensor_type = "atmotube"
        actual_cls = get.get_command_factory_cls(command_name=test_command_name, sensor_type=test_sensor_type)
        expected_cls = atm.AtmotubeFetchFactory
        self.assertEqual(actual_cls, expected_cls)

    def test_successfully_get_thingspeak_fetch_command_class(self):
        test_command_name = "fetch"
        test_sensor_type = "thingspeak"
        actual_cls = get.get_command_factory_cls(command_name=test_command_name, sensor_type=test_sensor_type)
        expected_cls = thnk.ThingspeakFetchFactory
        self.assertEqual(actual_cls, expected_cls)

    def test_exit_on_update_command_bad_sensor_type(self):
        test_command_name = "update"
        test_sensor_type = "bad sensor type"
        with self.assertRaises(SystemExit):
            get.get_command_factory_cls(command_name=test_command_name, sensor_type=test_sensor_type)

    def test_exit_on_init_command_bad_sensor_type_(self):
        test_command_name = "init"
        test_sensor_type = "bad sensor type"
        with self.assertRaises(SystemExit):
            get.get_command_factory_cls(command_name=test_command_name, sensor_type=test_sensor_type)

    def test_exit_on_fetch_command_bad_sensor_type(self):
        test_command_name = "fetch"
        test_sensor_type = "bad sensor type"
        with self.assertRaises(SystemExit):
            get.get_command_factory_cls(command_name=test_command_name, sensor_type=test_sensor_type)


if __name__ == '__main__':
    unittest.main()
