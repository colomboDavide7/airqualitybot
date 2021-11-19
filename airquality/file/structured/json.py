######################################################
#
# Author: Davide Colombo
# Date: 11/11/21 19:50
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import List
import airquality.file.util.parser as txt
import airquality.file.util.reader as read
import airquality.logger.loggable as log
import airquality.logger.util.decorator as log_decorator


def get_file_object(file_type: str, file_path: str, path_to_object: List[str] = (), log_filename="app"):

    if file_type == 'json':
        return JSONFile(file_path=file_path, path_to_object=path_to_object, log_filename=log_filename)
    else:
        raise SystemExit(f"'{get_file_object.__name__}()': bad 'file_type'={file_type}")


############################ FILE OBJECT BASE CLASS #############################
class FileObject(log.Loggable):

    def __init__(self, log_filename="app"):
        super(FileObject, self).__init__(log_filename=log_filename)

    @abc.abstractmethod
    def load(self):
        pass


############################ JSON FILE OBJECT CLASS #############################
class JSONFile(FileObject):

    def __init__(self, file_path: str, path_to_object: List[str] = (), log_filename="app"):
        super(JSONFile, self).__init__(log_filename=log_filename)
        self.file_path = file_path
        self.path_to_object = path_to_object
        self.content = None

    @log_decorator.log_decorator()
    def load(self):
        if self.content is not None:
            raise SystemExit(f"{JSONFile.__name__}: bad operation => cannot load file content multiple times")

        raw = read.open_read_close_file(self.file_path)                 # read raw file content
        text_parser = txt.get_text_parser(                              # get text parser
            file_ext='json',
            log_filename=self.log_filename)
        self.content = text_parser.parse(raw)                           # parse the raw content

        if self.path_to_object:                                         # search JSON object from 'path_to_object'
            self.content = self.content[self.path_to_object.pop()]      # get the content associated to the first object name
            for obj_name in self.path_to_object:                        # for each name in the 'path_to_object' argument
                self.content = self.content[obj_name]                   # apply a recursive search

    def __getattr__(self, item):
        if self.content is None:
            raise SystemExit(f"{JSONFile.__name__}: bad operation => you must load the file before getting its content")

        if item in self.content:
            return self.content[item]
        else:
            raise AttributeError(f"{JSONFile.__name__}: bad 'api.json' file structure => missing item='{item}'")
