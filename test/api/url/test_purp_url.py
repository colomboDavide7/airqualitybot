######################################################
#
# Author: Davide Colombo
# Date: 27/11/21 10:22
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.api.url.purpurl as url


class TestBaseURL(unittest.TestCase):

    def setUp(self) -> None:
        self.address = "some_address"

    def test_successfully_build_purpleair_url(self):
        test_key = "some_key"
        test_fields = ['f1', 'f2']
        test_options = {'opt1': 1, 'opt2': "abc"}
        test_bounding_box = {'x1': 1, 'y1': -1, 'x2': 3, 'y2': 2}
        builder = url.PurpleairURLBuilder(
            address=self.address, fields=test_fields, options=test_options, bounding_box=test_bounding_box, key=test_key
        )
        expected = "some_address?api_key=some_key&fields=f1,f2&x1=1&y1=-1&x2=3&y2=2&opt1=1&opt2=abc"
        actual = builder.build()
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
