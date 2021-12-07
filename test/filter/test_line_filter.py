######################################################
#
# Author: Davide Colombo
# Date: 03/12/21 17:35
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
from unittest.mock import Mock
import airquality.filter.linefilt as flt
import airquality.types.geonames as linetype


class TestLineFilter(unittest.TestCase):

    def setUp(self) -> None:
        self.repo_mock = Mock()

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
        self.repo_mock.lookup_place_names.return_value = ["pn1", "pn2"]
        line_filter = flt.LineFilter(repo=self.repo_mock)
        actual = line_filter.filter(self.generate_lines())
        self.assertEqual(next(actual).place_name, "pn3")

    def test_empty_lines_when_there_is_no_new_place(self):
        self.repo_mock.lookup_place_names.return_value = ["pn1", "pn2", "pn3"]
        line_filter = flt.LineFilter(repo=self.repo_mock)
        actual = line_filter.filter(self.generate_lines())
        with self.assertRaises(StopIteration):
            next(actual)


if __name__ == '__main__':
    unittest.main()
