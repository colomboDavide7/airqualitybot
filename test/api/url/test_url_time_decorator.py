######################################################
#
# Author: Davide Colombo
# Date: 27/11/21 10:29
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.api.url.timedecor as urldec
import airquality.api.url.dynurl as url
import airquality.types.timestamp as ts


class TestTimeURLDecorator(unittest.TestCase):

    def setUp(self) -> None:
        self.address = 'some_address'
        self.options = {'opt1': 1, 'opt2': "val"}

        self.test_atm_url = url.AtmotubeURLBuilder(address=self.address, options=self.options)
        self.test_atm_url.with_identifier('ident').with_api_key('some_key')

        self.test_thnk_url = url.ThingspeakURLBuilder(address=self.address, options=self.options, fmt='some_fmt')

    def test_successfully_decorate_atmotube_url_with_multiple_days_time_window(self):
        test_start_ts = ts.SQLTimestamp(timest='2021-10-11 08:45:00')
        test_stop_ts = ts.SQLTimestamp(timest='2021-10-13 20:45:00')

        decorator = urldec.AtmotubeURLTimeDecorator(to_decorate=self.test_atm_url, step_size_in_days=1)
        decorator.with_start_ts(start=test_start_ts).with_stop_ts(stop=test_stop_ts)

        actual = decorator.build()
        expected = "some_address?api_key=some_key&mac=ident&opt1=1&opt2=val&date=2021-10-11"
        self.assertEqual(actual, expected)
        self.assertTrue(decorator.has_next_date())

        actual = decorator.build()
        expected = "some_address?api_key=some_key&mac=ident&opt1=1&opt2=val&date=2021-10-12"
        self.assertEqual(actual, expected)
        self.assertTrue(decorator.has_next_date())

        actual = decorator.build()
        expected = "some_address?api_key=some_key&mac=ident&opt1=1&opt2=val&date=2021-10-13"
        self.assertEqual(actual, expected)
        self.assertFalse(decorator.has_next_date())

    def test_successfully_decorate_atmotube_url_with_single_day_time_window(self):
        test_start_ts = ts.SQLTimestamp(timest='2021-10-11 08:45:00')
        test_stop_ts = ts.SQLTimestamp(timest='2021-10-11 20:45:00')

        decorator = urldec.AtmotubeURLTimeDecorator(to_decorate=self.test_atm_url, step_size_in_days=1)
        decorator.with_start_ts(start=test_start_ts).with_stop_ts(stop=test_stop_ts)

        actual = decorator.build()
        expected = "some_address?api_key=some_key&mac=ident&opt1=1&opt2=val&date=2021-10-11"
        self.assertEqual(actual, expected)
        self.assertFalse(decorator.has_next_date())


if __name__ == '__main__':
    unittest.main()
