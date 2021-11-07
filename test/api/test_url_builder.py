#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 09:52
# @Description: unit test script
#
#################################################

import unittest
from airquality.api.url_builder import URLBuilderFactory, URLBuilderPurpleair


class TestURLBuilder(unittest.TestCase):

    def setUp(self) -> None:
        self.purpleair_url_builder_fact = URLBuilderFactory(url_builder_class=URLBuilderPurpleair)

    def test_successfully_build_purpleair_querystring(self):
        """Test the build of a valid purpleair URL querystring."""

        test_param = {"api_address": 'some_api_address', "api_key": "key", "fields": ["f1", "f2"], "opt": "val"}
        expected_output = "some_api_address?api_key=key&fields=f1,f2&opt=val"
        purpleair_builder = self.purpleair_url_builder_fact.create_url_builder()
        actual_output = purpleair_builder.build_url(parameters=test_param)
        self.assertEqual(actual_output, expected_output)

    def test_system_exit_when_building_purpleair_querystring(self):
        """Test SystemExit when missing required purpleair parameters for building URL querystring."""

        test_param = {"fields": "f1", "opt": "val"}
        purpleair_builder = self.purpleair_url_builder_fact.create_url_builder()
        with self.assertRaises(SystemExit):
            purpleair_builder.build_url(parameters=test_param)


if __name__ == '__main__':
    unittest.main()
