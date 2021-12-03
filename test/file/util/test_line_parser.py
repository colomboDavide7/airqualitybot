######################################################
#
# Author: Davide Colombo
# Date: 03/12/21 16:53
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.file.util.line_parser as parser


class TestLineParser(unittest.TestCase):

    def test_get_line_parser(self):
        tsv_parser = parser.get_line_parser(separator="\t")
        self.assertEqual(tsv_parser.__class__, parser.TSVLineParser)

        with self.assertRaises(SystemExit):
            parser.get_line_parser(separator="bad separator")

    def test_successfully_parse_lines(self):
        test_parser = parser.TSVLineParser(separator="\t")
        test_lines = ["t1\tt2\tt3\n", "t4\tt5\tt6\n"]
        actual = test_parser.parse_lines(test_lines)
        expected = [["t1", "t2", "t3"], ["t4", "t5", "t6"]]
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
