######################################################
#
# Author: Davide Colombo
# Date: 28/11/21 21:02
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.file.structured.fact as fact
import airquality.file.structured.json as jf


class TestStructuredFile(unittest.TestCase):

    def test_successfully_get_structured_file(self):
        test_content = {"some_object": "some value"}
        actual = fact.get_structured_file(file_fmt="json", parsed_content=test_content)
        expected_cls = jf.JSONFile
        self.assertEqual(actual.__class__, expected_cls)

    def test_successfully_get_structured_file_with_path_to_object(self):
        test_content = {
            "some_object": ["a", "b", "c"],
            "obj2": {"k1": "v1", "k2": "v2"}
        }

        test_path_to_object = ["obj2"]
        actual = fact.get_structured_file(file_fmt="json", path_to_object=test_path_to_object, parsed_content=test_content)
        self.assertEqual(actual.k1, "v1")
        self.assertEqual(actual.k2, "v2")

    def test_exit_on_bad_object_name(self):
        test_content = {
            "some_object": ["a", "b", "c"],
            "obj2": {"k1": "v1", "k2": "v2"}
        }

        test_path_to_object = ["some_object", "obj1"]
        with self.assertRaises(SystemExit):
            fact.get_structured_file(file_fmt="json", path_to_object=test_path_to_object, parsed_content=test_content)


if __name__ == '__main__':
    unittest.main()
