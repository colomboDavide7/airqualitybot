######################################################
#
# Author: Davide Colombo
# Date: 07/12/21 09:55
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
from unittest.mock import Mock
import airquality.database.repo.geolocation as dbrepo


class TestSensorGeoRepo(unittest.TestCase):

    def setUp(self) -> None:
        self.mocked_db_adapter = Mock()
        send_result_on_sensor_query = [(1, "n1"), (2, "n2")]
        send_result_on_geolocation_query_sensor_1 = [(9, 45)]
        send_result_on_geolocation_query_sensor_2 = [(9.5, 45.5)]
        self.mocked_db_adapter.send.side_effect = [
            send_result_on_sensor_query, send_result_on_geolocation_query_sensor_1, send_result_on_geolocation_query_sensor_2
        ]
        self.mocked_query_builder = Mock()
        self.mocked_query_builder.select_sensor_id_name_from_type.return_value = "some query for selecting ids and names"
        self.repo = dbrepo.SensorGeoRepository(
            db_adapter=self.mocked_db_adapter, query_builder=self.mocked_query_builder, sensor_type="purpleair"
        )

    def test_successfully_lookup_sensor_locations(self):
        actual = self.repo.lookup()
        self.assertEqual(len(actual), 2)
        self.assertEqual(actual[0].sensor_name, "n1")
        self.assertEqual(actual[0].geometry.as_text(), "POINT(9 45)")
        self.assertEqual(actual[1].sensor_name, "n2")
        self.assertEqual(actual[1].geometry.as_text(), "POINT(9.5 45.5)")

    def test_successfully_lookup_geolocation(self):
        self.mocked_db_adapter.send.side_effect = [[(9, 45)]]
        actual = self.repo.geometry_lookup(sensor_id=1)
        self.assertEqual(actual.as_text(), "POINT(9 45)")

    def test_empty_lookup(self):
        self.mocked_db_adapter.send.side_effect = [[]]
        actual = self.repo.lookup()
        self.assertEqual(len(actual), 0)

    def test_successfully_get_sensor_name2id(self):
        self.mocked_db_adapter.send.side_effect = [[(1, "n1"), (2, "n2")]]
        actual = self.repo.get_sensor_name2id()
        self.assertEqual(len(actual), 2)
        self.assertEqual(actual["n1"], 1)
        self.assertEqual(actual["n2"], 2)


if __name__ == '__main__':
    unittest.main()
