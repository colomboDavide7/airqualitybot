#################################################
#
# @Author: davidecolombo
# @Date: mar, 19-10-2021, 10:24
# @Description: Parser module defines the ParserFactory and the Parser
#               abstract class and its subclasses
#
#################################################
import builtins
import json
from typing import Dict, Any
from json.decoder import JSONDecodeError
from abc import ABC, abstractmethod


class Parser(ABC):
    """Abstract Base Class for all the Parser object supported in this
    application.

    - raw: (property) 'str' object that contains the raw content
    """
    def __init__(self, content: str):
        self.__raw = content

    @property
    def raw(self):
        """
        Need to be implemented as a @property, otherwise subclasses
        cannot access 'raw' variable in superclass.
        """
        return self.__raw

    @raw.setter
    def raw(self, value):
        """
        This method was defined with the only purpose of raising
        ValueError exception because 'raw' attribute cannot be set
        from outside.
        """
        raise ValueError("Cannot set the raw value.")

    @abstractmethod
    def parse(self) -> Dict[str, Any]:
        """
        Abstract method that a subclass must override for defining
        how to parse a file.
         """
        pass


class JSONParser(Parser):
    """JSONParser class defines the business rules for parsing JSON file
    format."""
    def __init__(self, content):
        super().__init__(content)
        self.__parsed = None

    def parse(self) -> Dict[str, Any]:
        """
        Parse raw content if parsed is None and return the parsed content.

        If the json file contains some error, a SystemExit exception is raised.
        """
        if self.__parsed is None:
            try:
                self.__parsed = json.loads(self.raw)
            except JSONDecodeError as jerr:
                raise SystemExit(f"{JSONParser.__name__}: "
                                 f"error while parsing JSON. "
                                 f"" + str(jerr))
        return self.__parsed

    @property
    def parsed(self):
        return self.__parsed

    @parsed.setter
    def parsed(self, value):
        """
        This method was defined with the only purpose of raising
        ValueError exception because 'parsed' attribute cannot be set
        from outside.
        """
        raise ValueError(f"{JSONParser.__name__} cannot set \'parsed\' "
                         f"value manually")


class ParserFactory(builtins.object):

    @staticmethod
    def make_parser_from_extension_file(file_extension: str,
                                        raw_content: str) -> Parser:
        if file_extension == 'json':
            return JSONParser(raw_content)
        else:
            raise TypeError(f"{ParserFactory.__name__}: "
                            f"unsupported file extension '{file_extension}'.")
