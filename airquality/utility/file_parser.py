#################################################
#
# @Author: davidecolombo
# @Date: mar, 19-10-2021, 10:24
# @Description: this script defines the classes for parsing file content from different extensions.
#
#################################################
import json
from typing import Dict, Any
from abc import ABC, abstractmethod
from json.decoder import JSONDecodeError
from airquality.constants.shared_constants import EMPTY_STRING


class FileParser(ABC):

    @abstractmethod
    def parse(self, raw_string: str) -> Dict[str, Any]:
        """Abstract method that defines the common interface for parsing raw string from file into Dict[str, Any]."""
        pass


class JSONFileParser(FileParser):
    """JSONFileParser class defines the business rules for parsing JSON file format."""

    def parse(self, raw_string: str) -> Dict[str, Any]:
        """Core method of this every FileParser instance that takes a raw string and parses it.

        If 'raw_string' is empty, SystemExit exception is raised.
        If some error occur while parsing the string, SystemExit exception is raised."""

        if raw_string == EMPTY_STRING:
            raise SystemExit(f"{JSONFileParser.__name__}: cannot parse empty raw string.")

        try:
            parsed = json.loads(raw_string)
        except JSONDecodeError as jerr:
            raise SystemExit(f"{JSONFileParser.__name__}: {str(jerr)}")
        return parsed


class FileParserFactory(object):
    """This class defines a @staticmethod for creating a FileParser object given the file extension."""

    @classmethod
    def file_parser_from_file_extension(cls, file_extension: str) -> FileParser:
        """Factory method for creating FileParser objects from file extension.

        If invalid file extension is passed, SystemExit is raised.

        Supported file extensions are: [ json ]."""

        if file_extension == 'json':
            return JSONFileParser()
        else:
            raise SystemExit(f"{FileParserFactory.__name__}: unknown {FileParser.__name__} for file extension "
                             f"'{file_extension}'.")
