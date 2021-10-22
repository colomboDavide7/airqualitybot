#################################################
#
# @Author: davidecolombo
# @Date: ven, 22-10-2021, 11:49
# @Description: unit test script
#
#################################################


import unittest
from airquality.picker.api_packet_picker import APIPacketPicket


class TestAPIPacketPicker(unittest.TestCase):


    def test_pick_atmotube_packet_without_geom(self):
        test_packet = [
            {"param1":  "value1",
             "time":    "a valid timestamp"
             }]

        test_param_id_code = {"param1": 1}

        expected_answer = [{f"{APIPacketPicket.PARAM_ID}": 1,
                            f"{APIPacketPicket.PARAM_VALUE}": "'value1'",
                            f"{APIPacketPicket.TIMESTAMP}": "'a valid timestamp'",
                            f"{APIPacketPicket.GEOMETRY}": "null"}]

        actual_answer = APIPacketPicket.pick_atmotube_api_packet(parsed_api_answer = test_packet, param_id_code = test_param_id_code)
        self.assertEqual(actual_answer, expected_answer)


if __name__ == '__main__':
    unittest.main()
