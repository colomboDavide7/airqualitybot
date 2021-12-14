######################################################
#
# Author: Davide Colombo
# Date: 14/12/21 20:17
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.file.parser.line_parser as parsertype


class TestLineParser(unittest.TestCase):

    def test_parse_tsv_lines(self):
        text_to_parse = "t1\tt2\tt3\nt4\tt5\tt6"
        tsv_parser = parsertype.TSVLineParser()
        actual = tsv_parser.parse(text_to_parse)

        first_line = next(actual)
        self.assertEqual(len(first_line), 3)
        self.assertEqual(first_line[0], "t1")
        self.assertEqual(first_line[1], "t2")
        self.assertEqual(first_line[2], "t3")

        second_line = next(actual)
        self.assertEqual(len(second_line), 3)
        self.assertEqual(second_line[0], "t4")
        self.assertEqual(second_line[1], "t5")
        self.assertEqual(second_line[2], "t6")

        with self.assertRaises(StopIteration):
            next(actual)

    def test_single_value_when_no_lines_are_present(self):
        text_to_parse = "this is an example of a wrong text to parse"
        tsv_parser = parsertype.TSVLineParser()
        actual = tsv_parser.parse(text_to_parse)
        first_line = next(actual)
        self.assertEqual(len(first_line), 1)
        self.assertEqual(first_line[0], "this is an example of a wrong text to parse")


if __name__ == '__main__':
    unittest.main()
