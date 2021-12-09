######################################################
#
# Author: Davide Colombo
# Date: 03/12/21 17:14
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import source.file.line.geonames as builder


class TestGeonamesLineBuilder(unittest.TestCase):

    def generate_lines(self):
        test_parsed_lines = [["cc", "pc", "pn", "st", "st_code", "pr", "pr_code", "", "", "45", "9"]]
        for line in test_parsed_lines:
            yield line

    def test_successfully_build_geonames_line(self):

        geonames_builder = builder.GeonamesLineBuilder()
        actual = geonames_builder.build_lines(self.generate_lines())
        item = next(actual)
        self.assertEqual(item.postal_code, "pc")
        self.assertEqual(item.country_code, "cc")
        self.assertEqual(item.place_name, "pn")
        self.assertEqual(item.state, "st")
        self.assertEqual(item.province, "pr")


if __name__ == '__main__':
    unittest.main()
