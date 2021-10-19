#################################################
#
# @Author: davidecolombo
# @Date: lun, 18-10-2021, 19:29
# @Description: a script for testing the resource_loader.py module
#
#################################################

import unittest
from airquality.app.resource_loader import ResourceLoader
from airquality.app.session import Session


class TestResourceLoader(unittest.TestCase):


    def setUp(self) -> None:
        self.path = "properties/resources.json"
        self.session = Session(settings = {})
        self.loader = ResourceLoader(
                path = self.path,
                session = self.session
        )

    def test_new_resource_loader(self):
        """Test create resource loader"""

        self.assertIsNotNone(self.loader)
        self.assertIsInstance(self.loader, ResourceLoader)

    def test_raise_ValueError_when_try_to_set_path(self):
        """Test ValueError when setting the path using setter method"""

        with self.assertRaises(ValueError):
            self.loader.path = "another/path/bad_file.txt"

    def test_load_resources(self):
        """Test loading the resource file locally."""

        response = self.loader.load_resources()
        self.assertTrue(response)

    def test_file_not_found(self):
        """Test FileNotFoundError when file does not exist."""

        path = "properties/bad_file.json"
        loader = ResourceLoader(path, session = self.session)
        with self.assertRaises(SystemExit):
            loader.load_resources()

    def test_parse_resources(self):
        """Test parse resources correct behaviour."""
        response = self.loader.load_resources()
        self.assertTrue(response)
        response = self.loader.parse_resources()
        self.assertTrue(response)

    def test_system_exit_when_raw_content_is_empty(self):
        """
        Test SystemExit when try to parse resources but raw content is empty.
        """
        with self.assertRaises(SystemExit):
            self.loader.parse_resources()

    def test_system_exit_while_parsing_resources(self):
        """Test SystemExit when parsing unsupported file extension.

        ATTENTION: THIS TEST WILL FAIL IF THE FILE
        'properties/text.txt' DOES NOT EXIST
        """

        path = "properties/test.txt"
        loader = ResourceLoader(path = path, session = self.session)
        try:
            response = loader.load_resources()
            self.assertTrue(response)
            with self.assertRaises(SystemExit):
                loader.parse_resources()
        except SystemExit as sysex:
            print("YOU MUST CREATE 'test.txt' file in 'properties' directory.")
            self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
