######################################################
#
# Author: Davide Colombo
# Date: 27/11/21 10:06
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.api.url.dynurl as url


class TestDynamicURL(unittest.TestCase):

    def setUp(self) -> None:
        self.address = "some_address"

    def test_successfully_build_atmotube_url(self):
        test_options = {'opt1': 'v1', 'opt2': 33}
        expected = "some_address?api_key=k&mac=m&opt1=v1&opt2=33"
        builder = url.AtmotubeURLBuilder(address=self.address, options=test_options)
        builder.with_identifier("m").with_api_key("k")
        actual = builder.build()
        self.assertEqual(actual, expected)

    def test_atmotube_url_without_external_options(self):
        test_options = {'opt1': 'v1', 'opt2': 33}
        expected = "some_address?api_key=None&mac=None&opt1=v1&opt2=33"
        builder = url.AtmotubeURLBuilder(address=self.address, options=test_options)
        actual = builder.build()
        self.assertEqual(actual, expected)

    def test_successfully_build_thingspeak_url(self):
        test_options = {'opt1': 'v1', 'opt2': 33}
        builder = url.ThingspeakURLBuilder(address=self.address, options=test_options, fmt='fmt')
        builder.with_identifier("id").with_api_key("k")
        expected = "some_address/id/feeds.fmt?api_key=k&opt1=v1&opt2=33"
        actual = builder.build()
        self.assertEqual(actual, expected)

    def test_thingspeak_url_without_external_options(self):
        test_options = {'opt1': 'v1', 'opt2': 33}
        builder = url.ThingspeakURLBuilder(address=self.address, options=test_options, fmt='fmt')
        expected = "some_address/None/feeds.fmt?api_key=None&opt1=v1&opt2=33"
        actual = builder.build()
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
