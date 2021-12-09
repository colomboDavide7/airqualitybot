######################################################
#
# Author: Davide Colombo
# Date: 07/12/21 08:32
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
from unittest.mock import Mock
import airquality.database.repo.info as dbrepo
import airquality.types.apiresp.inforesp as resptype


class TestSensorInfoRepo(unittest.TestCase):

    def setUp(self) -> None:
        self.mocked_db_adapter = Mock()
        self.mocked_db_adapter.send.return_value = [(1, "n1"), (2, "n2")]
        self.mocked_query_builder = Mock()
        self.mocked_query_builder.select_sensor_id_name_from_type.return_value = "some query for selecting ids and names"
        self.repo = dbrepo.SensorInfoRepository(
            db_adapter=self.mocked_db_adapter, query_builder=self.mocked_query_builder, sensor_type="purpleair"
        )

    def test_successfully_lookup_sensor(self):
        actual = self.repo.lookup()
        self.assertEqual(len(actual), 2)
        self.assertEqual(actual[0].sensor_name, "n1")
        self.assertEqual(actual[1].sensor_name, "n2")

    def test_successfully_get_max_sensor_id(self):
        self.mocked_db_adapter.send.return_value = [(None, )]
        actual = self.repo.max_sensor_id
        self.assertEqual(actual, 1)

        self.mocked_db_adapter.send.return_value = [(99, )]
        actual = self.repo.max_sensor_id
        self.assertEqual(actual, 100)

    # def test_successfully_push_sensor_responses(self):
    #     mocked_channel = Mock()
    #     mocked_channel.ch_key = "k"
    #     mocked_channel.ch_id = "id"
    #     mocked_channel.ch_name = "c1"
    #     mocked_channel.last_acquisition.get_formatted_timestamp.return_value = "2021-10-11 09:44:00"
    #
    #     mocked_geolocation = Mock()
    #     mocked_geolocation.geometry.geom_from_text.return_value = "ST_GeomFromText('POINT(9 45)', 26918)"
    #     mocked_geolocation.timestamp.get_formatted_timestamp.return_value = "2018-07-12 23:59:00"
    #
    #     test_response = [resptype.SensorInfoResponse(
    #         sensor_name="n1", sensor_type="t1", channels=mocked_channel, geolocation=mocked_geolocation)
    #     ]
    #
    #     self.repo.get_max_sensor_id()
    #     self.repo.push(test_response)


if __name__ == '__main__':
    unittest.main()
