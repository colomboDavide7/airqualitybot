######################################################
#
# Author: Davide Colombo
# Date: 28/12/21 15:53
# Description: INSERT HERE THE DESCRIPTION
#
######################################################


class HelpException(Exception):
    pass


class ProgramError(Exception):

    def __init__(self, msg: str, cause: str):
        self.msg = msg
        self.cause = cause

    def __repr__(self):
        return f"{type(self).__name__}(msg='{self.msg}', cause='{self.cause}')"


class PersonalityError(ProgramError):
    pass


class MissingArgumentError(ProgramError):
    pass


class DatabaseAdapterError(ProgramError):
    pass
