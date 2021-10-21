#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 08:10
# @Description: unit test script
#
#################################################

import unittest
from airquality.api.api_request_adapter import APIRequestAdapterFactory


class TestAPIRequestAdapter(unittest.TestCase):

    def test_system_exit_when_missing_api_address(self):
        api_req = APIRequestAdapterFactory.create_api_request_adapter("atmotube")
        with self.assertRaises(SystemExit):
            api_req.fetch("ciao=hello")

    def test_system_exit_fetch(self):
        """Test SystemExit when invalid URL is given."""

        api_req = APIRequestAdapterFactory.create_api_request_adapter("atmotube")
        api_req.api_address = "bad_api_address"
        with self.assertRaises(SystemExit):
            api_req.fetch("ciao=hello")

    def test_system_exit_with_invalid_personality(self):

        with self.assertRaises(SystemExit):
            APIRequestAdapterFactory.create_api_request_adapter("bad_bot_personality")


if __name__ == '__main__':
    unittest.main()
