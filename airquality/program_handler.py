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
from contextlib import suppress
from collections import namedtuple
from urllib.error import HTTPError, URLError


class Option(namedtuple('Option', ['pers', 'short_name', 'long_name'])):

    def __str__(self):
        return f"{self.short_name},{self.long_name}"

    def __repr__(self):
        return f"{type(self).__name__}(personality={self.pers}, short_name={self.short_name}, long_name={self.long_name})"


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
        if exc_type in (ValueError, KeyError, HTTPError, URLError):
            print(f"{type(self).__name__} in __exit__(): {exc_val!r}")
            sys.exit(1)

    @property
    def program_usage_message(self) -> str:
        return environ['program_usage_msg'].format(pers='|'.join(self.valid_personalities), opt='|'.join(f"{opt!s}" for opt in self.options))

    @property
    def valid_personalities(self) -> List[str]:
        if not self._valid_pers:
            self._valid_pers = environ['valid_personalities'].split(',')
        return self._valid_pers

    @property
    def options(self) -> List[Option]:
        if not self._options:
            for pers in self.valid_personalities:
                with suppress(KeyError):
                    short_name, long_name = environ[f'{pers}_opt'].split(',')
                    self._options.append(Option(pers=pers, short_name=short_name, long_name=long_name))
        return self._options

    @property
    def personality(self) -> str:
        p = self._args[0]
        if p not in self.valid_personalities:
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
