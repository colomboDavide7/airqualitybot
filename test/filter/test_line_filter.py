######################################################
#
# Author: Davide Colombo
# Date: 03/12/21 17:35
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.filter.linefilt as flt
import airquality.types.geonames as linetype


class TestLineFilter(unittest.TestCase):

    def setUp(self) -> None:
        self.line_filter = flt.LineFilter()
        self.test_responses = [
            linetype.GeonamesLine(place_name="pn1", postal_code="", country_code="", state="", province="", geom=None),
            linetype.GeonamesLine(place_name="pn1", postal_code="", country_code="", state="", province="", geom=None),
            linetype.GeonamesLine(place_name="pn2", postal_code="", country_code="", state="", province="", geom=None),
            linetype.GeonamesLine(place_name="pn3", postal_code="", country_code="", state="", province="", geom=None),
            linetype.GeonamesLine(place_name="pn1", postal_code="", country_code="", state="", province="", geom=None),
            linetype.GeonamesLine(place_name="pn3", postal_code="", country_code="", state="", province="", geom=None)
        ]

    def generate_lines(self):
        for line in self.test_responses:
            yield line

    def test_successfully_filter_lines(self):
        test_place_names = ["pn1", "pn2"]
        self.line_filter.with_database_place_names(test_place_names)
        actual = self.line_filter.filter(self.generate_lines())
        self.assertEqual(next(actual).place_name, "pn3")

    def test_empty_lines_when_there_is_no_new_place(self):
        test_place_names = ["pn1", "pn2", "pn3"]
        self.line_filter.with_database_place_names(test_place_names)
        actual = self.line_filter.filter(self.generate_lines())
        with self.assertRaises(StopIteration):
            next(actual)


if __name__ == '__main__':
    unittest.main()
