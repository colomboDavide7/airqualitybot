######################################################
#
# Author: Davide Colombo
# Date: 27/11/21 16:07
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.api.resp.measure as resp


class TestThingspeakMeasureResponse(unittest.TestCase):

    def setUp(self) -> None:
        self.thnk_resp_builder = resp.ThingspeakAPIRespBuilder()

    def test_exit_on_missing_channel_name(self):
        test_parsed_response = {
            'channel': {},
            'feeds': [
                {"created_at": "2019-01-20T23:59:30Z",
                 "entry_id": 148009,
                 "field1": "9793.20",
                 "field2": "2817.47",
                 "field3": "463.51",
                 "field4": "52.36",
                 "field5": "15.56",
                 "field6": "2.58",
                 "field7": "52.31",
                 "field8": "99.89"}
            ]
        }

        with self.assertRaises(SystemExit):
            self.thnk_resp_builder.build(test_parsed_response)


if __name__ == '__main__':
    unittest.main()
