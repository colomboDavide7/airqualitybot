######################################################
#
# Author: Davide Colombo
# Date: 31/12/21 08:10
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
# from airquality.environment import Environment
# from airquality.runner import Runner
# import sys
#
#
# class WrongUsageError(Exception):
#     """
#     An *Exception* that defines the type of error raised when the application is used in the wrong way.
#     """
#
#     def __init__(self, cause: str):
#         self.cause = cause
#
#     def __repr__(self):
#         return f"{type(self).__name__}(cause={self.cause})"
#
#
# def main():
#     try:
#         args = sys.argv[1:]
#         if not args:
#             raise WrongUsageError("expected at least one argument!")
#
#         env = Environment()
#         personality = args[0]
#         if personality not in env.valid_personalities:
#             raise WrongUsageError(f"expected '{personality}' to be one of {env.valid_personalities}")
#
#         if personality == 'purpleair':
#             with PurpleairRunner():
#                 pass
#
#     except WrongUsageError as err:
#         print(repr(err))
#         print(env.program_usage_msg)
