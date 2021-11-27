######################################################
#
# Author: Davide Colombo
# Date: 27/11/21 15:41
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.api.resp.measure as resp
import airquality.types.timestamp as ts
import airquality.types.postgis as pgis


class TestMeasureResponse(unittest.TestCase):

    def setUp(self) -> None:
        self.atm_resp_builder = resp.AtmotubeMeasureBuilder()
        self.thnk_resp_builder = resp.ThingspeakMeasureBuilder()

    def test_successfully_build_atmotube_response(self):
        test_channel_name = 'main'
        self.atm_resp_builder.with_channel_name(test_channel_name)

        test_parsed_response = {
            "data": {
                "items": [
                    {"time": "2021-11-17T00:01:00.000Z",
                     "voc": 0.86,
                     "pm1": 9,
                     "pm25": 10,
                     "pm10": 11,
                     "t": 25,
                     "h": 32,
                     "p": 1009.13},
                    {"time": "2021-11-17T19:57:00.000Z",
                     "voc": 0.84,
                     "pm1": 54,
                     "pm25": 58,
                     "pm10": 60,
                     "t": 14,
                     "h": 42,
                     "p": 1011.06,
                     "coords": {
                         "lat": 44.818836,
                         "lon": 20.4538335
                     }}
                ]
            }
        }

        # Build the response
        responses = self.atm_resp_builder.build(test_parsed_response)

        # Take the first (and unique) response in the list of responses
        for i in range(len(responses)):
            # Take the i-th item
            test_item = test_parsed_response['data']['items'][i]
            # Take the i-th resp
            actual_resp = responses[i]

            # Test time consistency
            self.assertEqual(actual_resp.timestamp.ts, ts.AtmotubeTimestamp(timest=test_item['time']).ts)
            # Test geometry consistency
            if test_item.get('coords') is None:
                self.assertEqual(actual_resp.geometry.as_text(), "NULL")
            else:
                test_geom = pgis.PostgisPoint(lat=test_item['coords']['lat'], lng=test_item['coords']['lon'])
                self.assertEqual(actual_resp.geometry.as_text(), test_geom.as_text())
            # Test measures consistency
            measures = actual_resp.measures
            for m in measures:
                self.assertEqual(m.value, test_item[m.name])

    def test_system_exit_when_no_sensor_name_was_set(self):
        test_parsed_response = {
            "data": {
                "items": [
                    {"time": "2021-11-17T00:01:00.000Z",
                     "voc": 0.86,
                     "pm1": 9,
                     "pm25": 10,
                     "pm10": 11,
                     "t": 25,
                     "h": 32,
                     "p": 1009.13},
                    {"time": "2021-11-17T19:57:00.000Z",
                     "voc": 0.84,
                     "pm1": 54,
                     "pm25": 58,
                     "pm10": 60,
                     "t": 14,
                     "h": 42,
                     "p": 1011.06,
                     "coords": {
                         "lat": 44.818836,
                         "lon": 20.4538335
                     }}
                ]
            }
        }

        with self.assertRaises(SystemExit):
            self.atm_resp_builder.build(test_parsed_response)


if __name__ == '__main__':
    unittest.main()
