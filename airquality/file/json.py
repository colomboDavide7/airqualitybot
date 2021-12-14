######################################################
#
# Author: Davide Colombo
# Date: 11/11/21 19:50
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import json
from typing import List


# ------------------------------- JSONFile ------------------------------- #
class JSONFile(object):

    def __init__(self, path_to_file: str, path_to_object: List[str] = ()):
        raw = self._read_file(path_to_file)
        parsed_content = json.loads(raw)
        self.content = parsed_content
        if path_to_object:
            self._recursive_search(path_to_object)

    ################################ _read_file() ################################
    def _read_file(self, path_to_file):
        try:
            with open(path_to_file, "r") as f:
                return f.read()
        except FileNotFoundError as err:
            raise SystemExit(f"{self.__class__.__name__} catches {err.__class__.__name__} in {self._read_file.__name__} => {err!r}")

    ################################ _recursive_search() ################################
    def _recursive_search(self, path_to_object: List[str]):
        try:
            for obj_name in path_to_object:
                self.content = self.content[obj_name]
        except KeyError as err:
            raise SystemExit(f"{self.__class__.__name__} catches {err.__class__.__name__} in {self._recursive_search.__name__} => {err!r}")

    ################################ __getattr__() ################################
    def __getattr__(self, item):
        try:
            return self.content[item]
        except KeyError as err:
            raise SystemExit(f"{self.__class__.__name__} catches {err.__class__.__name__} in {self.__getattr__.__name__} => {err!r}")
        except TypeError as err:
            raise SystemExit(f"{self.__class__.__name__} catches {err.__class__.__name__} in {self.__getattr__.__name__} => "
                             f"{type(self.content)}, required <class '{dict.__name__}'>")
