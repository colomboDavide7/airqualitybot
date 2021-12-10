######################################################
#
# Author: Davide Colombo
# Date: 10/12/21 10:57
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import api as apirequest


class TestAPIRequest(unittest.TestCase):

    def test_system_exit_when_bad_url_is_passed(self):
        request = apirequest.APIRequest()
        with self.assertRaises(SystemExit):
            request.fetch_from_url("bad url")

    def test_system_exit_when_url_error_occurs(self):
        request = apirequest.APIRequest()
        with self.assertRaises(SystemExit):
            request.fetch_from_url("https://www.google")


if __name__ == '__main__':
    unittest.main()
