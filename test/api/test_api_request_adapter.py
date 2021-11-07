#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 08:10
# @Description: unit test script
#
#################################################

import unittest
from airquality.api.urllib_adapter import UrllibAdapter


class TestAPIRequestAdapter(unittest.TestCase):

    def test_system_exit_fetch(self):
        """Test SystemExit when invalid URL is given."""

        api_req = UrllibAdapter("bad_api_address")
        with self.assertRaises(SystemExit):
            api_req.fetch("ciao=hello")


if __name__ == '__main__':
    unittest.main()
