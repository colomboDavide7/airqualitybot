######################################################
#
# Author: Davide Colombo
# Date: 21/12/21 11:18
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from os import listdir
from os.path import join, isfile
from unittest import TestCase, main
from airquality.filedict import FrozenFileDict

TEST_DIRECTORY = "test_resources"


class TestFrozenFileDict(TestCase):

    def setUp(self) -> None:
        self.all_files = [f for f in listdir(TEST_DIRECTORY) if isfile(join(TEST_DIRECTORY, f)) and not f.startswith('.')]

    def test_invalid_path_to_dir(self):
        """Test NotADirectoryError when call __init__() with invalid 'path_to_dir' argument."""

        with self.assertRaises(NotADirectoryError):
            FrozenFileDict(path_to_dir="bad/dir/path", include=[])

    def test_include_files(self):
        """Test that the only available files are those included."""

        file_dict = FrozenFileDict(path_to_dir=TEST_DIRECTORY, include=["ES.txt"])
        self.assertEqual(file_dict.all_files, self.all_files)
        expected_included_files = ["ES.txt"]
        self.assertEqual(file_dict.included_files, expected_included_files)
        self.assertEqual(len(file_dict), 1)
        print(file_dict['ES.txt'])

    def test_get_invalid_file_content(self):
        """Test KeyError when call __getitem__() with a filename that is not included (and also does not exist)."""

        file_dict = FrozenFileDict(path_to_dir=TEST_DIRECTORY, include=["ES.txt"])
        with self.assertRaises(KeyError):
            print(file_dict['IT.txt'])

    def test_empty_included_files(self):
        file_dict = FrozenFileDict(path_to_dir=TEST_DIRECTORY, include=[])
        self.assertEqual(len(file_dict), 0)


if __name__ == '__main__':
    main()
