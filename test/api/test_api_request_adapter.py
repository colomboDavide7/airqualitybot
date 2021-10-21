#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 08:10
# @Description: This script contains the test for the api_request_adapter.py module
#
#################################################

import unittest
from airquality.api.api_request_adapter import AtmotubeAPIRequestAdapterFactory


class TestAPIRequestAdapter(unittest.TestCase):

    def setUp(self) -> None:
        self.bad_api_address = "bad_address"
        self.atmo_api_factory = AtmotubeAPIRequestAdapterFactory()

    def test_system_exit_fetch(self):
        """Test SystemExit when invalid URL is given."""

        api_req = self.atmo_api_factory.create_api_request_adapter(self.bad_api_address)
        with self.assertRaises(SystemExit):
            api_req.fetch("ciao=hello")


if __name__ == '__main__':
    unittest.main()
