######################################################
#
# Author: Davide Colombo
# Date: 27/11/21 10:06
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import source.api.url.private as url


class TestDynamicURL(unittest.TestCase):

    def setUp(self) -> None:
        self.test_atm_url_template = "some_address?api_key={api_key}&mac={mac}&order=asc&format={fmt}"
        self.test_atm_url_template_with_options = "some_address?api_key={api_key}&mac={mac}&order=asc&format={fmt}&opt1=v1&opt2=33"
        self.test_thnk_url_template = "some_address/{channel_id}/feeds.{fmt}?api_key={api_key}"
        self.test_thnk_url_template_with_options = "some_address/{channel_id}/feeds.{fmt}?api_key={api_key}&opt1=v1&opt2=33"

    def test_successfully_build_atmotube_url(self):
        builder = url.AtmotubeURLBuilder(self.test_atm_url_template)
        builder.with_api_response_fmt("fmt").with_identifier("m").with_api_key("k")
        actual = builder.build()
        expected = "some_address?api_key=k&mac=m&order=asc&format=fmt"
        self.assertEqual(actual, expected)

    def test_successfully_build_atmotube_url_with_options(self):
        builder = url.AtmotubeURLBuilder(self.test_atm_url_template_with_options)
        builder.with_api_response_fmt("fmt").with_api_key("k").with_identifier("m")
        actual = builder.build()
        expected = "some_address?api_key=k&mac=m&order=asc&format=fmt&opt1=v1&opt2=33"
        self.assertEqual(actual, expected)

    def test_successfully_build_thingspeak_url(self):
        builder = url.ThingspeakURLBuilder(self.test_thnk_url_template)
        builder.with_api_response_fmt("fmt").with_identifier("id").with_api_key("k")
        expected = "some_address/id/feeds.fmt?api_key=k"
        actual = builder.build()
        self.assertEqual(actual, expected)

    def test_successfully_build_thingspeak_url_with_options(self):
        builder = url.ThingspeakURLBuilder(self.test_thnk_url_template_with_options)
        builder.with_api_response_fmt("fmt").with_api_key("k").with_identifier("id")
        actual = builder.build()
        expected = "some_address/id/feeds.fmt?api_key=k&opt1=v1&opt2=33"
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
