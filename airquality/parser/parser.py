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


class Parser(ABC):

    @abstractmethod
    def parse(self, raw_string: str) -> Dict[str, Any]:
        """
        Abstract method that defines the common interface for parsing
        raw string into Dict[str, Any]."""
        pass


class JSONParser(Parser):
    """
    JSONParser class defines the business rules for parsing JSON file
    format."""

    def parse(self, raw_string: str) -> Dict[str, Any]:

        if not raw_string:
            raise SystemExit(f"{JSONParser.__name__}: cannot parse empty raw string.")

        try:
            parsed = json.loads(raw_string)
        except JSONDecodeError as jerr:
            raise SystemExit(f"{JSONParser.__name__}: {str(jerr)}")

        return parsed


class ParserFactory(builtins.object):
    """
    This class defines a @staticmethod for creating a Parser object given
    the file extension.

    For now, JSON is the only supported file type."""

    @staticmethod
    def make_parser_from_extension_file(file_extension: str) -> Parser:
        """Factory method for creating Parser instances from file extension.

        If invalid file extension is passed, SystemExit is raised."""

        if file_extension == 'json':
            return JSONParser()
        else:
            raise SystemExit(f"{ParserFactory.__name__}: unknown parser for file extension '{file_extension}'.")
