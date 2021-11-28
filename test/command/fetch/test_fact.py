######################################################
#
# Author: Davide Colombo
# Date: 28/11/21 17:57
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.command.fetch.fact as fact
import airquality.command.fetch.atmfact as atm
import airquality.command.fetch.thnkfact as thnk


class TestFetchFactory(unittest.TestCase):

    def test_successfully_get_atmotube_factory_class(self):
        test_sensor_type = "atmotube"
        actual_cls = fact.get_fetch_factory_cls(sensor_type=test_sensor_type)
        expected_cls = atm.AtmotubeFetchFactory
        self.assertEqual(actual_cls, expected_cls)

    def test_successfully_get_thingspeak_factory_class(self):
        test_sensor_type = "thingspeak"
        actual_cls = fact.get_fetch_factory_cls(sensor_type=test_sensor_type)
        expected_cls = thnk.ThingspeakFetchFactory
        self.assertEqual(actual_cls, expected_cls)

    def test_exit_on_bad_sensor_type(self):
        test_sensor_type = "bad sensor type"
        with self.assertRaises(SystemExit):
            fact.get_fetch_factory_cls(sensor_type=test_sensor_type)


if __name__ == '__main__':
    unittest.main()
