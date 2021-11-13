######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 11/11/21 19:50
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List
import airquality.io.reader as read
import airquality.utility.parser.text as txt


class JSONFile:

    def __init__(self, file_path: str, path_to_object: List[str] = ()):
        raw = read.open_read_close_file(file_path)          # read raw file content
        text_parser_cls = txt.get_parser_class('json')      # get text parser class
        self.content = text_parser_cls(raw).parse()         # parse the raw content

        if path_to_object:                                      # search JSON object from 'path_to_object'
            self.content = self.content[path_to_object.pop()]   # get the content associated to the first object name
            for obj_name in path_to_object:                     # for each name in the 'path_to_object' argument
                self.content = self.content[obj_name]           # apply a recursive search

    def __getattr__(self, item):
        if item in self.content:
            return self.content[item]
        else:
            raise AttributeError(f"{JSONFile.__name__}: bad 'api.json' file structure => missing item='{item}'")
