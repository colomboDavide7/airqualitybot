######################################################
#
# Author: Davide Colombo
# Date: 23/12/21 09:22
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from unittest import TestCase, main
from airquality.fileline import ParsedFileLine, GeonamesLine, PoscodeLine


class TestFileLine(TestCase):

    def test_ValueError_on_wrong_line_limit(self):
        """Test ValueError when the number of tokens in *line* does not match the *line_limit* parameter."""

        with self.assertRaises(ValueError):
            ParsedFileLine(line="some wrong line", line_limit=3)

    def test_ValueError_on_wrong_line_separator(self):
        """Test ValueError when a wrong *separator* is used. The *separator* argument defaults to '\\t'."""

        with self.assertRaises(ValueError):
            ParsedFileLine(line="a, b, c", line_limit=3)

    def test_successfully_parse_line(self):
        line = ParsedFileLine(line="a, b, c", line_limit=3, separator=", ")
        self.assertEqual(len(line.line), 3)
        print(repr(line))

    def test_successfully_parse_geonames_line(self):
        test_line = "ES	04001	Almeria	Andalucia	AN	Almeria	AL	Almeria	04013	36.8381	-2.4597	4"
        geoline = GeonamesLine(line=test_line)
        self.assertEqual(len(geoline.line), 12)
        self.assertEqual(geoline.poscode, "04001")
        self.assertEqual(geoline.country, "ES")
        self.assertEqual(geoline.geom, "ST_GeomFromText('POINT(-2.4597 36.8381)', 26918)")
        self.assertEqual(geoline.state, "Andalucia")
        self.assertEqual(geoline.province, "Almeria")
        self.assertEqual(geoline.place, "Almeria")
        print(repr(geoline))

    def test_successfully_parse_poscode_line(self):
        test_line = "04001"
        poscode_line = PoscodeLine(line=test_line, line_limit=1)
        self.assertEqual(len(poscode_line.line), 1)
        self.assertEqual(poscode_line.poscode, "04001")
        print(repr(poscode_line))


if __name__ == '__main__':
    main()
