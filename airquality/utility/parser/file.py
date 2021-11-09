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
from airquality.core.constants.shared_constants import EXCEPTION_HEADER


class FileParser(abc.ABC):

    @abc.abstractmethod
    def parse(self, text: str) -> Dict[str, Any]:
        pass


class JSONFileParser(FileParser):

    def parse(self, text: str) -> Dict[str, Any]:
        try:
            return json.loads(text)
        except json.decoder.JSONDecodeError as je:
            raise SystemExit(f"{EXCEPTION_HEADER} {JSONFileParser.__name__} bad json schema => {je!s}")


class FileParserFactory(object):

    @staticmethod
    def make_parser(file_extension: str) -> FileParser:
        if file_extension == 'json':
            return JSONFileParser()
        else:
            raise SystemExit(
                f"{EXCEPTION_HEADER} {FileParserFactory.__name__} bad file extension => '{file_extension}' is not supported"
            )
