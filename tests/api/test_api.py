#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 08:10
# @Description: This script contains the tests for the api.py module
#
#################################################

import unittest
from airquality.api.api import AtmotubeAPIRequest, AtmotubeAPIRequestFactory


class TestAPI(unittest.TestCase):

    def setUp(self) -> None:
        self.api_address = "https://api.atmotube.com/api/v1/data"
        self.query_string = "api_key=8d2faf68-ed6a-4964-89bd-f0a94c047181&mac=ee:6e:82:c4:a0:58&offset=0&order=desc&date=2021-10-11"
        self.bad_api_address = "bad_address"
        self.atmo_api_factory = AtmotubeAPIRequestFactory()

    def test_atmotube_api_request(self):
        """Test creation of the atmotube API request"""
        api_req = self.atmo_api_factory.create_request(self.api_address)
        self.assertIsNotNone(api_req)
        self.assertIsInstance(api_req, AtmotubeAPIRequest)

    def test_fetch(self):
        """Test fetch data from Atmotube API."""
        api_req = self.atmo_api_factory.create_request(self.api_address)
        data = api_req.fetch(self.query_string)
        self.assertIsNotNone(data)

    def test_system_exit_fetch(self):
        """Test SystemExit when invalid URL is given."""
        api_req = self.atmo_api_factory.create_request(self.bad_api_address)
        with self.assertRaises(SystemExit):
            api_req.fetch("ciao=hello")


if __name__ == '__main__':
    unittest.main()
