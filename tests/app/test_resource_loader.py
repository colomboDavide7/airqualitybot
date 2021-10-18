#################################################
#
# @Author: davidecolombo
# @Date: lun, 18-10-2021, 19:29
# @Description: a script for testing the resource_loader.py module
#
#################################################

import unittest
from airquality.app.resource_loader import ResourceLoader

class TestResourceLoader(unittest.TestCase):

    def test_new_resource_loader(self):
        """Test create resource loader"""

        valid_path = "properties/resources.json"
        loader = ResourceLoader(valid_path)
        self.assertIsNotNone(loader)
        self.assertIsInstance(loader, ResourceLoader)

    def test_raise_ValueError_when_try_to_set_path(self):
        """Test ValueError when setting the path using setter method"""

        valid_path = "properties/resources.json"
        loader = ResourceLoader(valid_path)
        with self.assertRaises(ValueError):
            loader.path = "another/path/bad_file.txt"

if __name__ == '__main__':
    unittest.main()
