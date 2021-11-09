#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 08:10
# @Description: unit test script
#
#################################################

import unittest
from io.remote.api.adapter import UrllibAdapter


class TestAPIRequestAdapter(unittest.TestCase):

    def test_system_exit_when_invalid_url_is_used(self):
        with self.assertRaises(SystemExit):
            UrllibAdapter.fetch(url="bad url")


if __name__ == '__main__':
    unittest.main()
