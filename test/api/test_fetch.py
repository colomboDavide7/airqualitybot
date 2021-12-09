#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 08:10
# @Description: unit test script
#
#################################################
import unittest
import source.api.req.api_req as fetch


class TestAPIRequestAdapter(unittest.TestCase):

    def test_system_exit_when_invalid_url_is_used(self):
        with self.assertRaises(SystemExit):
            fetch.fetch_from_url("https://bad_address.com?bad_param")


if __name__ == '__main__':
    unittest.main()
