######################################################
#
# Author: Davide Colombo
# Date: 28/12/21 15:44
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import sys
from typing import List
from airquality.env import Option
from airquality.exc import MissingArgumentError, HelpException, PersonalityError


class ArgsHandler(object):

    def __init__(self, valid_pers: List[str], valid_options: List[Option]):
        self.valid_pers = valid_pers
        self.valid_options = valid_options
        self._args = sys.argv[1:]
        if len(self._args) < 1:
            raise MissingArgumentError(msg="Expected at least 1 argument", cause=str(self._args))

    def __repr__(self):
        return f"{type(self).__name__}(args={self._args}, valid_personalities={self.valid_pers!r}, valid_options={self.valid_options!r})"

    @property
    def personality(self) -> str:
        p = self._args[0]
        if p == 'help':
            raise HelpException()
        if p not in self.valid_pers:
            raise PersonalityError(msg=f"Expected '{p}' to be one of {self.valid_pers}", cause=p)
        return p

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
                    else:
                        print(f"WARNING: ignore unknown option '{opt}'")
        return inserted_options
