######################################################
#
# Author: Davide Colombo
# Date: 23/12/21 10:22
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import sys
from os import environ
from typing import List
from dotenv import load_dotenv
from collections import namedtuple
from urllib.error import HTTPError, URLError


class Option(namedtuple('Option', ['pers', 'short_name', 'long_name'])):

    def __str__(self):
        if self.short_name and self.long_name:
            return f"{self.short_name},{self.long_name}"
        return ""

    def __repr__(self):
        return f"{type(self).__name__}(personality={self.pers}, short_name={self.short_name}, long_name={self.long_name})"


class HelpException(Exception):
    pass


class ProgramHandler(object):

    def __init__(self):
        self._valid_pers = []
        self._options = []
        self._args = sys.argv[1:]
        if len(self._args) < 1:
            raise ValueError(f"{type(self).__name__} expected at least 1 argument, got {len(self._args)}")

    def __enter__(self):
        load_dotenv(dotenv_path='.env')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type == HelpException:
            print(self.program_usage_message)
            sys.exit(1)

        if exc_type in (ValueError, KeyError, HTTPError, URLError):
            print(f"{type(self).__name__} in __exit__(): {exc_val!r}")
            sys.exit(1)

    @property
    def program_usage_message(self) -> str:
        pers = ' | '.join(f"{opt.pers} [{opt!s}]" for opt in self.valid_options)
        return environ['program_usage_msg'].format(pers=pers)

    @property
    def valid_personalities(self) -> List[str]:
        if not self._valid_pers:
            self._valid_pers = environ['valid_personalities'].split(',')
        return self._valid_pers

    @property
    def options(self) -> List[Option]:
        program_options = self._args[1:]
        inserted_options = []
        if program_options:
            valid_options = [opt for opt in self.valid_options if opt.pers == self.personality]
            for opt in program_options:
                for valid in valid_options:
                    if opt == valid.short_name or opt == valid.long_name:
                        inserted_options.append(valid)
        return inserted_options

    @property
    def valid_options(self) -> List[Option]:
        if not self._options:
            for pers in self.valid_personalities:
                try:
                    short_name, long_name = environ[f'{pers}_opt'].split(',')
                    self._options.append(Option(pers=pers, short_name=short_name, long_name=long_name))
                except KeyError:
                    self._options.append(Option(pers=pers, short_name="", long_name=""))
        return self._options

    @property
    def personality(self) -> str:
        p = self._args[0]
        if p == 'help':
            raise HelpException()

        if p not in self.valid_personalities:
            print(self.program_usage_message)
            raise ValueError(f"Expected '{p}' to be one of: {self.valid_personalities!r}")
        return p

    @property
    def dbname(self) -> str:
        return environ['database']

    @property
    def user(self) -> str:
        return environ['user']

    @property
    def password(self) -> str:
        return environ['password']

    @property
    def host(self) -> str:
        return environ['host']

    @property
    def port(self) -> str:
        return environ['port']
