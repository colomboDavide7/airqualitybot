######################################################
#
# Author: Davide Colombo
# Date: 23/12/21 10:22
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import os
import sys
from typing import List
from dotenv import load_dotenv
from collections import namedtuple
from urllib.error import HTTPError, URLError
from airquality.exc import ProgramError, HelpException


class Option(namedtuple('Option', ['pers', 'short_name', 'long_name'])):

    def __str__(self):
        if self.short_name and self.long_name:
            return f"{self.short_name},{self.long_name}"
        return ""

    def __repr__(self):
        return f"{type(self).__name__}(personality={self.pers}, short_name={self.short_name}, long_name={self.long_name})"


class Environment(object):

    def __init__(self):
        self._valid_pers = []
        self._valid_options = []

    def __enter__(self):
        load_dotenv(dotenv_path='.env')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            if issubclass(exc_type, ProgramError):
                print(f"{type(self).__name__} in __exit__(): {exc_val!r}")
                sys.exit(1)
            if exc_type == HelpException:
                print(self.program_usage_message)
                sys.exit(0)
            if exc_type in (ValueError, KeyError, HTTPError, URLError):
                print(f"{type(self).__name__} in __exit__(): {exc_val!r}")
                sys.exit(1)
        print("success")

    def __repr__(self):
        return f"{type(self).__name__}()"

    @property
    def program_usage_message(self) -> str:
        pers = ' | '.join(f"{opt.pers} [{opt!s}]" for opt in self.valid_options)
        return os.environ['program_usage_msg'].format(pers=pers)

    @property
    def valid_personalities(self) -> List[str]:
        if not self._valid_pers:
            self._valid_pers = os.environ['valid_personalities'].split(',')
        return self._valid_pers

    @property
    def valid_options(self) -> List[Option]:
        if not self._valid_options:
            for pers in self.valid_personalities:
                try:
                    short_name, long_name = os.environ[f'{pers}_opt'].split(',')
                    self._valid_options.append(Option(pers=pers, short_name=short_name, long_name=long_name))
                except KeyError:
                    self._valid_options.append(Option(pers=pers, short_name="", long_name=""))
        return self._valid_options

    @property
    def dbname(self) -> str:
        return os.environ['database']

    @property
    def user(self) -> str:
        return os.environ['user']

    @property
    def password(self) -> str:
        return os.environ['password']

    @property
    def host(self) -> str:
        return os.environ['host']

    @property
    def port(self) -> str:
        return os.environ['port']
