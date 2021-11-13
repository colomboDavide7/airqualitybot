#################################################
#
# @Author: davidecolombo
# @Date: lun, 25-10-2021, 11:00
# @Description: unit test script
#
#################################################
import unittest
import airquality.api.util.extractor as extr


class TestAPIExtractor(unittest.TestCase):

    def test_extract_purpleair_data(self):
        test_api_answer = {
            'fields': ["name", "sensor_index"],
            'data': [
                ["n1", "idx1"],
                ["n2", "idx2"]
            ]
        }

        expected_answer = [{"name": "n1", "sensor_index": "idx1"}, {"name": "n2", "sensor_index": "idx2"}]
        actual_answer = extr.PurpleairAPIExtractor(test_api_answer).extract()
        self.assertEqual(actual_answer, expected_answer)

    def test_extract_empty_list_purpleair(self):
        test_api_answer = {
            'fields': ["f1", "f2"],
            'data': []
        }
        expected_answer = []
        actual_answer = extr.PurpleairAPIExtractor(test_api_answer).extract()
        self.assertEqual(actual_answer, expected_answer)

    ################################ TEST THINGSPEAK EXTRACTOR ################################

    def test_successfully_extract_thingspeak_data(self):
        test_api_answer = {"feeds": [
                               {"created_at": "2021-10-27T05:36:59Z",
                                "field1": "42.35",
                                "field2": "63.05",
                                "field3": "76.32",
                                "field6": "50",
                                "field7": "60"},
                               {"created_at": "2021-10-27T05:38:59Z",
                                "field1": "41.07",
                                "field2": "61.54",
                                "field3": "70.31",
                                "field6": "50",
                                "field7": "60"}
                           ]}

        expected_answer = [
            {"created_at": "2021-10-27T05:36:59Z",
             'fields': [{'name': 'pm1.0_atm_a', 'value': '42.35'},
                        {'name': 'pm2.5_atm_a', 'value': '63.05'},
                        {'name': 'pm10.0_atm_a', 'value': '76.32'},
                        {'name': 'temperature_a', 'value': '50'},
                        {'name': 'humidity_a', 'value': '60'}],
             },
            {"created_at": "2021-10-27T05:38:59Z",
             'fields': [{'name': 'pm1.0_atm_a', 'value': '41.07'},
                        {'name': 'pm2.5_atm_a', 'value': '61.54'},
                        {'name': 'pm10.0_atm_a', 'value': '70.31'},
                        {'name': 'temperature_a', 'value': '50'},
                        {'name': 'humidity_a', 'value': '60'}],
             }]

        actual_output = extr.ThingspeakAPIExtractor(test_api_answer, channel_name="1A").extract()
        self.assertEqual(actual_output, expected_answer)

    def test_extract_empty_list_thingspeak(self):
        test_api_answer = {"channel": {'param1': 'val1'},
                           "feeds": []}
        expected_answer = []
        actual_output = extr.ThingspeakAPIExtractor(test_api_answer, channel_name="1A").extract()
        self.assertEqual(actual_output, expected_answer)

    ################################ TEST ATMOTUBE EXTRACTOR ################################

    def test_successfully_extract_atmotube_data(self):
        test_api_answer = {"data": {"items":
                                    [{'time': "2021-10-02T00:00:00.000Z"},
                                     {'time': "2021-10-02T00:01:00.000Z"}]
                                    }
                           }

        expected_output = [{'time': "2021-10-02T00:00:00.000Z"}, {'time': "2021-10-02T00:01:00.000Z"}]
        actual_output = extr.AtmotubeAPIExtractor(test_api_answer).extract()
        self.assertEqual(actual_output, expected_output)

    def test_extract_empty_list_atmotube(self):
        test_api_answer = {"data": {"items": []}}
        expected_output = []
        actual_output = extr.AtmotubeAPIExtractor(test_api_answer).extract()
        self.assertEqual(actual_output, expected_output)


if __name__ == '__main__':
    unittest.main()
