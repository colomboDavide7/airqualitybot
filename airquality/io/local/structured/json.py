######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 11/11/21 19:50
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import json
from typing import List
import airquality.io.local.io as io


class JSONFile:

    def __init__(self, file: str, path_to_object: List[str] = ()):
        """Initialize a JSONFile object by reading the content of the 'file' and by parsing it. In addition, if the
        'path_to_object' argument is not empty, it is recursively searched (and saved) only the required object."""

        raw = io.open_read_close_file(file)
        self.content = json.loads(raw)

        if path_to_object:
            self.content = self.content[path_to_object.pop()]
            for obj_name in path_to_object:
                self.content = self.content[obj_name]

    def __getattr__(self, item):
        if item in self.content:
            return self.content[item]
        else:
            raise AttributeError(f"{JSONFile.__name__} bad attribute => {item}")
