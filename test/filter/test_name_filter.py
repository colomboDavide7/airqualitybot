######################################################
#
# Author: Davide Colombo
# Date: 27/11/21 17:39
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.filter.namefilt as flt
import airquality.types.apiresp.inforesp as resp


class TestNameFilter(unittest.TestCase):

    def setUp(self) -> None:
        self.test_responses = [
            resp.SensorInfoResponse(sensor_name="n1", sensor_type="t1", channels=[], geolocation=None),
            resp.SensorInfoResponse(sensor_name="n2", sensor_type="t1", channels=[], geolocation=None),
            resp.SensorInfoResponse(sensor_name="n3", sensor_type="t1", channels=[], geolocation=None)
        ]

    def test_successfully_filter_names(self):
        resp_filter = flt.NameFilter()
        resp_filter.with_database_sensor_names(["n2"])
        actual = resp_filter.filter(resp2filter=self.test_responses)
        self.assertEqual(next(actual).sensor_name, "n1")
        self.assertEqual(next(actual).sensor_name, "n3")
        with self.assertRaises(StopIteration):
            next(actual)

    def test_empty_filtered_list(self):
        resp_filter = flt.NameFilter()
        resp_filter.with_database_sensor_names(["n1", "n2", "n3"])
        actual = resp_filter.filter(resp2filter=self.test_responses)
        with self.assertRaises(StopIteration):
            next(actual)


if __name__ == '__main__':
    unittest.main()
