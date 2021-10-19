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

    def test_open_read_close_resource_file(self):
        """Test loading the resource file locally."""

        response = self.loader.open_read_close()
        self.assertTrue(response)

    def test_file_not_found(self):
        """Test if the loader returns False when file does not exist."""

        path = "properties/bad_file.json"
        loader = ResourceLoader(path, session = self.session)
        with self.assertRaises(SystemExit):
            loader.open_read_close()

if __name__ == '__main__':
    unittest.main()
