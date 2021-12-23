######################################################
#
# Author: Davide Colombo
# Date: 21/12/21 10:55
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from os import listdir
from typing import List
from os.path import join, isfile, isdir
from collections.abc import Mapping
from airquality.fileline import ParsedFileLine


class FrozenFileDict(Mapping):

    def __init__(self, path_to_dir: str, include: List[str], line_factory=ParsedFileLine):
        if not isdir(path_to_dir):
            raise NotADirectoryError(f"{type(self).__name__} expected '{path_to_dir}' to be a directory!")
        self.path_to_dir = path_to_dir
        self.line_factory = line_factory
        self.include = include
        self._all = []
        self._included = []

    @property
    def all_files(self) -> List[str]:
        if not self._all:
            self._all = [f for f in listdir(self.path_to_dir) if isfile(join(self.path_to_dir, f)) and not f.startswith('.')]
        return self._all

    @property
    def included_files(self):
        if not self._included:
            self._included = [f for f in self.all_files if f in self.include]
        return self._included

    def __getitem__(self, filename):
        if filename not in self.included_files:
            raise KeyError(f"{type(self).__name__} in __getitem__(): expected '{filename}' to be one of: [{self.included_files!r}]")
        fullname = join(self.path_to_dir, filename)
        with open(fullname, 'r') as f:
            return (self.line_factory(line) for line in f.read().split('\n') if line)

    def __iter__(self):
        return iter(self.included_files)

    def __len__(self):
        return len(self.included_files)

    def __repr__(self):
        return f"{type(self).__name__}(path_to_dir={self.path_to_dir}, include={self.include}, " \
               f"all_files={self.all_files}, included_files={self.included_files})"
