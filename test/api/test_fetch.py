#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 08:10
# @Description: unit test script
#
#################################################
import unittest
import api.util.request as api


class TestAPIRequestAdapter(unittest.TestCase):

    def test_system_exit_when_invalid_url_is_used(self):
        with self.assertRaises(SystemExit):
            api.fetch("https://bad_address.com?bad_param")


if __name__ == '__main__':
    unittest.main()
