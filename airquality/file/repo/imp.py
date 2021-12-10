######################################################
#
# Author: Davide Colombo
# Date: 07/12/21 20:15
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from os import listdir
from os.path import isfile, join
from typing import Tuple
import airquality.file.repo.abc as repoabc


# ------------------------------- FileRepo ------------------------------- #
class FileRepo(repoabc.FileRepoABC):

    def __init__(self, path2directory: str):
        self._path2directory = path2directory
        self._files = tuple([f for f in listdir(self._path2directory) if isfile(join(self._path2directory, f)) and not f.startswith('.')])

    ################################ get_files() ################################
    def read_all(self) -> Tuple[str]:
        file_contents = []
        for f in self._files:
            fullname = join(self._path2directory, f)
            with open(fullname, "r") as fd:
                file_contents.append(fd.read())
        return tuple(file_contents)

    ################################ get_file_from_filename() ################################
    def read_file(self, filename: str) -> str:
        try:
            fullname = join(self._path2directory, filename)
            with open(fullname, "f") as fd:
                return fd.read()
        except FileNotFoundError as err:
            raise SystemExit(f"{self.__class__.__name__} catches {err.__class__.__name__} exception => {err!r}")
