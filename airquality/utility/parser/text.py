#################################################
#
# @Author: davidecolombo
# @Date: mar, 19-10-2021, 10:24
# @Description: this script defines the classes for parsing file content from different extensions.
#
#################################################
import abc
import json
from typing import Dict, Any


def get_parser_class(file_ext: str):

    if file_ext == 'json':
        return JSONParser
    else:
        raise SystemExit(f"'{get_parser_class.__name__}()': bad file extension => '{file_ext}' is not supported")


class TextParser(abc.ABC):

    def __init__(self, text: str):
        self.text = text

    @abc.abstractmethod
    def parse(self) -> Dict[str, Any]:
        pass


class JSONParser(TextParser):

    def __init__(self, text: str):
        super(JSONParser, self).__init__(text)

    def parse(self) -> Dict[str, Any]:
        try:
            return json.loads(self.text)
        except json.decoder.JSONDecodeError as je:
            raise SystemExit(f"{JSONParser.__name__} bad json schema => {je!s}")
