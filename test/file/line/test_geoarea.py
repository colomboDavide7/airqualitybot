######################################################
#
# Author: Davide Colombo
# Date: 03/12/21 17:14
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.file.line.geoarea as geobuilder


class TestGeoareaLineBuilder(unittest.TestCase):

    def setUp(self) -> None:
        self.geoarea_line_builder = geobuilder.GeoareaLineBuilder()

    def generate_lines(self):
        test_parsed_lines = [["cc", "pc", "pn", "st", "st_code", "pr", "pr_code", "", "", "45", "9"]]
        for line in test_parsed_lines:
            yield line

    def generate_wrong_lines(self):
        test_parsed_lines = [["", "", "", "", "", "", "", "", "", "", ""]]
        for line in test_parsed_lines:
            yield line

    def test_successfully_build_geonames_line(self):
        actual = self.geoarea_line_builder.build(self.generate_lines())
        item = next(actual)
        self.assertEqual(item.postal_code(), "pc")
        self.assertEqual(item.country_code(), "cc")
        self.assertEqual(item.place_name(), "pn")
        self.assertEqual(item.state(), "st")
        self.assertEqual(item.province(), "pr")
        with self.assertRaises(StopIteration):
            next(actual)

    def test_system_exit_when_index_error_occurs(self):
        actual = self.geoarea_line_builder.build(self.generate_wrong_lines())
        item = next(actual)
        with self.assertRaises(SystemExit):
            item.country_code()
        with self.assertRaises(SystemExit):
            item.postal_code()
        with self.assertRaises(SystemExit):
            item.place_name()
        with self.assertRaises(SystemExit):
            item.state()
        with self.assertRaises(SystemExit):
            item.province()
        with self.assertRaises(SystemExit):
            item.geolocation()


if __name__ == '__main__':
    unittest.main()
