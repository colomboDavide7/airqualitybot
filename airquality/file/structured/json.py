######################################################
#
# Author: Davide Colombo
# Date: 11/11/21 19:50
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List, Dict, Any
import airquality.file.structured.file as file


class JSONFile(file.StructuredFile):

    def __init__(self, parsed_content: Dict[str, Any], path_to_object: List[str] = (), log_filename="log"):
        super(JSONFile, self).__init__(log_filename=log_filename)
        self.content = parsed_content
        if path_to_object:                                              # search JSON object from 'path_to_object'
            self.content = parsed_content[path_to_object.pop()]    # get the content associated to the first object name
            for obj_name in path_to_object:                             # for each name in the 'path_to_object' argument
                self.content = self.content[obj_name]

    def __getattr__(self, item):
        if item in self.content:
            return self.content[item]
        else:
            raise AttributeError(f"{JSONFile.__name__}: bad 'api.json' file structure => missing item='{item}'")
