######################################################
#
# Author: Davide Colombo
# Date: 03/12/21 17:14
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.file.line.geobuilder as builder


class TestGeonamesLineBuilder(unittest.TestCase):

    def test_successfully_build_geonames_line(self):
        test_parsed_lines = [["cc", "pc", "pn", "st", "st_code", "pr", "pr_code"]]
        geonames_builder = builder.GeonamesLineBuilder()
        actual = geonames_builder.build_lines(test_parsed_lines)
        self.assertEqual(actual[0].postal_code, "pc")
        self.assertEqual(actual[0].country_code, "cc")
        self.assertEqual(actual[0].place_name, "pn")
        self.assertEqual(actual[0].state, "st")
        self.assertEqual(actual[0].province, "pr")


if __name__ == '__main__':
    unittest.main()
