######################################################
#
# Author: Davide Colombo
# Date: 03/12/21 17:35
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.filter.geonames as flt
import airquality.types.line.line as linetype


class TestLineFilter(unittest.TestCase):

    def setUp(self) -> None:
        self.test_responses = [
            linetype.GeonamesLine(place_name="pn1", postal_code="27100", country_code="", state="", province="", geom=None),
            linetype.GeonamesLine(place_name="pn2", postal_code="98010", country_code="", state="", province="", geom=None),
            linetype.GeonamesLine(place_name="pn3", postal_code="34109", country_code="", state="", province="", geom=None)
        ]

    def generate_lines(self):
        for line in self.test_responses:
            yield line

    def test_filter_lines_without_constraints(self):
        line_filter = flt.GeonamesFilter()
        actual = line_filter.filter(self.generate_lines())
        self.assertEqual(next(actual).place_name, "pn1")
        self.assertEqual(next(actual).place_name, "pn2")
        self.assertEqual(next(actual).place_name, "pn3")
        with self.assertRaises(StopIteration):
            next(actual)

    def test_successfully_filter_out_places_already_present_into_database(self):
        line_filter = flt.GeonamesFilter()
        line_filter.with_database_place_names(["pn1", "pn2"])
        actual = line_filter.filter(self.generate_lines())
        self.assertEqual(next(actual).place_name, "pn3")

    def test_empty_lines_when_there_is_no_new_place(self):
        line_filter = flt.GeonamesFilter()
        line_filter.with_database_place_names(["pn1", "pn2", "pn3"])
        actual = line_filter.filter(self.generate_lines())
        with self.assertRaises(StopIteration):
            next(actual)

    def test_successfully_keep_only_patient_postal_codes(self):
        line_filter = flt.GeonamesFilter()
        line_filter.with_postalcodes(["27100"])
        actual = line_filter.filter(self.generate_lines())
        self.assertEqual(next(actual).postal_code, "27100")
        with self.assertRaises(StopIteration):
            next(actual)

    def test_successfully_keep_new_places_at_patient_poscodes(self):
        line_filter = flt.GeonamesFilter()
        line_filter.with_postalcodes(["27100", "98010"])
        line_filter.with_database_place_names(["pn1"])
        actual = line_filter.filter(self.generate_lines())
        item = next(actual)
        self.assertEqual(item.place_name, "pn2")
        self.assertEqual(item.postal_code, "98010")
        with self.assertRaises(StopIteration):
            next(actual)

    def test_empty_list_for_combination_of_new_places_and_patient_poscodes(self):
        line_filter = flt.GeonamesFilter()
        line_filter.with_postalcodes(["27100", "98010"])
        line_filter.with_database_place_names(["pn1", "pn2"])
        actual = line_filter.filter(self.generate_lines())
        with self.assertRaises(StopIteration):
            next(actual)


if __name__ == '__main__':
    unittest.main()
