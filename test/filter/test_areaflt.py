######################################################
#
# Author: Davide Colombo
# Date: 03/12/21 17:35
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.filter.areaflt as filtertype
import airquality.file.line.geoarea as linetype


class TestGeoareaFilter(unittest.TestCase):

    def setUp(self) -> None:
        self.test_responses = [
            linetype.GeoareaLineType(line=["", "27100", "pn1"]),
            linetype.GeoareaLineType(line=["", "98010", "pn2"]),
            linetype.GeoareaLineType(line=["", "34109", "pn3"]),
        ]

    def generate_lines(self):
        for line in self.test_responses:
            yield line

    def test_filter_lines_without_constraints(self):
        line_filter = filtertype.GeoareaFilter(places=[])
        actual = line_filter.filter(self.generate_lines())
        self.assertEqual(next(actual).place_name(), "pn1")
        self.assertEqual(next(actual).place_name(), "pn2")
        self.assertEqual(next(actual).place_name(), "pn3")
        with self.assertRaises(StopIteration):
            next(actual)

    def test_new_places(self):
        line_filter = filtertype.GeoareaFilter(places=["pn1", "pn2"])
        actual = line_filter.filter(self.generate_lines())
        self.assertEqual(next(actual).place_name(), "pn3")

    def test_new_places_output_empty_list(self):
        line_filter = filtertype.GeoareaFilter(places=["pn1", "pn2", "pn3"])
        actual = line_filter.filter(self.generate_lines())
        with self.assertRaises(StopIteration):
            next(actual)

    def test_patient_postalcodes(self):
        line_filter = filtertype.GeoareaFilter(postalcodes=["27100"], places=[])
        actual = line_filter.filter(self.generate_lines())
        self.assertEqual(next(actual).postal_code(), "27100")
        with self.assertRaises(StopIteration):
            next(actual)

    def test_successfully_keep_new_places_at_patient_postalcode(self):
        line_filter = filtertype.GeoareaFilter(postalcodes=["27100", "98010"], places=["pn1"])
        actual = line_filter.filter(self.generate_lines())
        item = next(actual)
        self.assertEqual(item.place_name(), "pn2")
        self.assertEqual(item.postal_code(), "98010")
        with self.assertRaises(StopIteration):
            next(actual)

    def test_new_places_plus_postalcodes_output_empty_list(self):
        line_filter = filtertype.GeoareaFilter(postalcodes=["27100", "98010"], places=["pn1", "pn2"])
        actual = line_filter.filter(self.generate_lines())
        with self.assertRaises(StopIteration):
            next(actual)


if __name__ == '__main__':
    unittest.main()
