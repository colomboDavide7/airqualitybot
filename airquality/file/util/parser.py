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


def get_text_parser(file_ext: str):

    if file_ext == 'json':
        return JSONParser()
    else:
        raise SystemExit(f"'{get_text_parser.__name__}()': bad file extension => '{file_ext}' is not supported")


class TextParser(abc.ABC):

    @abc.abstractmethod
    def parse(self, text: str) -> Dict[str, Any]:
        pass


class JSONParser(TextParser):

    def parse(self, text: str) -> Dict[str, Any]:
        try:
            return json.loads(text)
        except json.decoder.JSONDecodeError as je:
            raise SystemExit(f"{JSONParser.__name__}: bad json schema => {je!s}")
