#################################################
#
# @Author: davidecolombo
# @Date: ven, 22-10-2021, 11:49
# @Description: unit test script
#
#################################################


import unittest
from airquality.picker import TIMESTAMP, PARAM_VALUE, PARAM_ID, GEOMETRY
from airquality.picker.api_packet_picker import APIPacketPicket


class TestAPIPacketPicker(unittest.TestCase):


    def test_pick_atmotube_packet_without_geom(self):
        test_packet = [
            {"param1":  "value1",
             "time":    "2021-10-11T09:44:00.000Z"
             }]

        test_param_id_code = {"param1": 1}

        expected_answer = [{f"{PARAM_ID}": 1,
                            f"{PARAM_VALUE}": "'value1'",
                            f"{TIMESTAMP}": "'2021-10-11 09:44:00'",
                            f"{GEOMETRY}": "null"}]

        actual_answer = APIPacketPicket.pick_atmotube_api_packet(
                parsed_api_answer = test_packet,
                param_id_code = test_param_id_code
        )
        self.assertEqual(actual_answer, expected_answer)


if __name__ == '__main__':
    unittest.main()
