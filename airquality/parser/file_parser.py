#################################################
#
# @Author: davidecolombo
# @Date: mar, 19-10-2021, 10:24
# @Description: Parser module defines the ParserFactory and the Parser
#               abstract class and its subclasses
#
#################################################
import json
import builtins
from typing import Dict, Any
from abc import ABC, abstractmethod
from json.decoder import JSONDecodeError


class FileParser(ABC):

    @abstractmethod
    def parse(self, raw_string: str) -> Dict[str, Any]:
        """
        Abstract method that defines the common interface for parsing
        raw string from file into Dict[str, Any]."""
        pass


class JSONFileParser(FileParser):
    """
    JSONFileParser class defines the business rules for parsing JSON file
    format."""

    def parse(self, raw_string: str) -> Dict[str, Any]:

        if not raw_string:
            raise SystemExit(f"{JSONFileParser.__name__}: cannot parse empty raw string.")

        try:
            parsed = json.loads(raw_string)
        except JSONDecodeError as jerr:
            raise SystemExit(f"{JSONFileParser.__name__}: {str(jerr)}")

        return parsed


class FileParserFactory(builtins.object):
    """
    This class defines a @staticmethod for creating a Parser object given
    the file extension.

    For now, JSON is the only supported file type."""

    @staticmethod
    def file_parser_from_file_extension(file_extension: str) -> FileParser:
        """Factory method for creating Parser instances from file extension.

        If invalid file extension is passed, SystemExit is raised."""

        if file_extension == 'json':
            return JSONFileParser()
        else:
            raise SystemExit(f"{FileParserFactory.__name__}: unknown parser for file extension '{file_extension}'.")
