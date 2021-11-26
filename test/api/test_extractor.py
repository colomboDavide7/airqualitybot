#################################################
#
# @Author: davidecolombo
# @Date: lun, 25-10-2021, 11:00
# @Description: unit test script
#
#################################################
import unittest
import airquality.api.util.extractor as extr
import airquality.api.config as extr_const
import airquality.to_delete.config as adapt_const


class TestAPIExtractor(unittest.TestCase):

    def setUp(self) -> None:
        self.purpleair_extractor = extr.PurpleairSensorDataExtractor()
        self.atmotube_extractor = extr.AtmotubeSensorDataExtractor()
        self.thingspeak_extractor = extr.ThingspeakMeasureBuilder()

    def test_extract_purpleair_data(self):
        test_api_answer = {
            'fields': ["name", "sensor_index"],
            'data': [
                ["n1", "idx1"],
                ["n2", "idx2"]
            ]
        }

        expected_answer = [{"name": "n1", "sensor_index": "idx1"}, {"name": "n2", "sensor_index": "idx2"}]
        actual_answer = self.purpleair_extractor.uniform(parsed_response=test_api_answer)
        self.assertEqual(actual_answer, expected_answer)

    def test_extract_empty_list_purpleair(self):
        test_api_answer = {
            'fields': ["f1", "f2"],
            'data': []
        }
        expected_answer = []
        actual_answer = self.purpleair_extractor.uniform(parsed_response=test_api_answer)
        self.assertEqual(actual_answer, expected_answer)

    def test_exit_on_missing_data_item(self):
        test_api_answer = {'fields': ["f1", "f2"]}
        with self.assertRaises(SystemExit):
            self.purpleair_extractor.uniform(parsed_response=test_api_answer)

    def test_exit_on_missing_fields_item(self):
        test_api_answer = {'data': [['p1', 'p2', 'p3'], ['p4', 'p5', 'p6']]}
        with self.assertRaises(SystemExit):
            self.purpleair_extractor.uniform(parsed_response=test_api_answer)

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
             extr_const.CHANNEL_FIELDS: [{extr_const.FIELD_NAME: 'pm1.0_atm_a', extr_const.FIELD_VALUE: '42.35'},
                                         {extr_const.FIELD_NAME: 'pm2.5_atm_a', extr_const.FIELD_VALUE: '63.05'},
                                         {extr_const.FIELD_NAME: 'pm10.0_atm_a', extr_const.FIELD_VALUE: '76.32'},
                                         {extr_const.FIELD_NAME: 'temperature_a', extr_const.FIELD_VALUE: '50'},
                                         {extr_const.FIELD_NAME: 'humidity_a', extr_const.FIELD_VALUE: '60'}],
             },
            {"created_at": "2021-10-27T05:38:59Z",
             extr_const.CHANNEL_FIELDS: [{extr_const.FIELD_NAME: 'pm1.0_atm_a', extr_const.FIELD_VALUE: '41.07'},
                                         {extr_const.FIELD_NAME: 'pm2.5_atm_a', extr_const.FIELD_VALUE: '61.54'},
                                         {extr_const.FIELD_NAME: 'pm10.0_atm_a', extr_const.FIELD_VALUE: '70.31'},
                                         {extr_const.FIELD_NAME: 'temperature_a', extr_const.FIELD_VALUE: '50'},
                                         {extr_const.FIELD_NAME: 'humidity_a', extr_const.FIELD_VALUE: '60'}],
             }]

        actual_output = self.thingspeak_extractor.uniform(parsed_response=test_api_answer, channel_name=adapt_const.FST_CH_A)
        self.assertEqual(actual_output, expected_answer)

    def test_extract_empty_list_thingspeak(self):
        test_api_answer = {"channel": {'param1': 'val1'},
                           "feeds": []}
        expected_answer = []
        actual_output = self.thingspeak_extractor.uniform(parsed_response=test_api_answer, channel_name=adapt_const.FST_CH_A)
        self.assertEqual(actual_output, expected_answer)

    def test_exit_on_missing_feeds(self):
        test_api_answer = {"channel": {'param1': 'val1'}}
        with self.assertRaises(SystemExit):
            self.thingspeak_extractor.uniform(parsed_response=test_api_answer, channel_name=adapt_const.FST_CH_A)

    def test_exit_on_missing_created_at_data_item(self):
        test_api_answer = {"channel": {'param1': 'val1'},
                           "feeds": [{'other': 'v'}]}
        with self.assertRaises(SystemExit):
            self.thingspeak_extractor.uniform(parsed_response=test_api_answer, channel_name=adapt_const.FST_CH_A)

    def test_system_exit_when_missing_channel_name_thingspeak_extractor(self):
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

        with self.assertRaises(SystemExit):
            self.thingspeak_extractor.uniform(parsed_response=test_api_answer, channel_name="bad name")

        with self.assertRaises(SystemExit):
            self.thingspeak_extractor.uniform(parsed_response=test_api_answer)

    ################################ TEST ATMOTUBE EXTRACTOR ################################

    def test_successfully_extract_atmotube_data(self):
        test_api_answer = {"data": {"items": [{'time': "2021-10-02T00:00:00.000Z"}, {'time': "2021-10-02T00:01:00.000Z"}]}}

        expected_output = [{'time': "2021-10-02T00:00:00.000Z"}, {'time': "2021-10-02T00:01:00.000Z"}]
        actual_output = self.atmotube_extractor.uniform(parsed_response=test_api_answer)
        self.assertEqual(actual_output, expected_output)

    def test_extract_empty_list_atmotube(self):
        test_api_answer = {"data": {"items": []}}
        expected_output = []
        actual_output = self.atmotube_extractor.uniform(parsed_response=test_api_answer)
        self.assertEqual(actual_output, expected_output)

    def test_exit_on_missing_atmotube_data_item(self):
        test_api_answer = {'some': 'v'}
        with self.assertRaises(SystemExit):
            self.atmotube_extractor.uniform(parsed_response=test_api_answer)

    def test_exit_on_missing_atmotube_items_within_data_item(self):
        test_api_answer = {"data": {"other": 'v'}}
        with self.assertRaises(SystemExit):
            self.atmotube_extractor.uniform(parsed_response=test_api_answer)


if __name__ == '__main__':
    unittest.main()
