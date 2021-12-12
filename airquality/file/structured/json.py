######################################################
#
# Author: Davide Colombo
# Date: 11/11/21 19:50
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import json
from typing import List
import airquality.file.structured.file as file


class JSONFile(file.StructuredFile):

    def __init__(self, path_to_file: str, path_to_object: List[str] = (), log_filename="log"):
        super(JSONFile, self).__init__(log_filename=log_filename)
        with open(path_to_file, "r") as f:
            raw = f.read()

        parsed_content = json.loads(raw)
        self.content = parsed_content
        if path_to_object:
            first_object = path_to_object.pop()
            self._exit_on_bad_object(first_object)
            self.content = parsed_content[first_object]

            # recursive search
            for obj_name in path_to_object:
                self._exit_on_bad_object(obj_name)
                self.content = self.content[obj_name]

    def _exit_on_bad_object(self, obj_name: str):
        if obj_name not in self.content:
            raise SystemExit(f"{JSONFile.__name__}: ")

    def __getattr__(self, item):
        if item in self.content:
            return self.content[item]
        else:
            raise AttributeError(f"{JSONFile.__name__}: bad 'api.json' file structure => missing item='{item}'")
