######################################################
#
# Author: Davide Colombo
# Date: 28/11/21 17:53
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.command.init.fact as fact


class TestInitFactory(unittest.TestCase):

    def test_successfully_get_init_class(self):
        test_sensor_type = "purpleair"
        actual_cls = fact.get_init_factory_cls(sensor_type=test_sensor_type)
        expected_cls = fact.PurpleairInitFactory
        self.assertEqual(actual_cls, expected_cls)

    def test_exit_on_bad_sensor_type(self):
        test_sensor_type = "bad sensor type"
        with self.assertRaises(SystemExit):
            fact.get_init_factory_cls(sensor_type=test_sensor_type)


if __name__ == '__main__':
    unittest.main()
