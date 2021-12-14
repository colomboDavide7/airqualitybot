######################################################
#
# Author: Davide Colombo
# Date: 21/11/21 10:43
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import sys
from typing import List, Tuple
import airquality.env.getfact as dispatcher


################################ main() ################################
def main():

    try:
        command, target = get_commandline_arguments(sys.argv[1:])
        env_fact = dispatcher.get_env_fact(path_to_env='.env', command=command, target=target)
        env = env_fact.craft_env()
        env.run()
    except SystemExit as ex:
        print(repr(ex))
        sys.exit(1)


################################ get_commandline_arguments() ################################
def get_commandline_arguments(args: List[str]) -> Tuple[str, str]:
    validate_arguments(args=args)
    command, target = args
    validate_command(command=command)
    validate_target(target=target)

    return command, target


################################ validate_arguments() ################################
def validate_arguments(args: List[str]) -> None:
    if not args:
        print(PROGRAM_DESCRIPTION)
        raise SystemExit(f"ERROR: {validate_arguments.__name__}(): bad usage => missing required arguments")
    if len(args) != 2:
        print(PROGRAM_DESCRIPTION)
        raise SystemExit(f"ERROR: {validate_arguments.__name__}(): bad usage => wrong number of arguments")


################################ validate_command() ################################
def validate_command(command: str) -> None:
    valid_commands = ["init", "update", "fetch"]
    if command not in valid_commands:
        print(PROGRAM_DESCRIPTION)
        raise SystemExit(f"ERROR: {validate_command.__name__}: bad command => VALID COMMANDS: [{'|'.join(c for c in valid_commands)}]")


################################ validate_target() ################################
def validate_target(target: str) -> None:
    valid_targets = ["atmotube", "purpleair", "thingspeak", "geonames"]
    if target not in valid_targets:
        print(PROGRAM_DESCRIPTION)
        raise SystemExit(f"ERROR: {validate_target.__name__}(): bad target => VALID TARGETS: [{'|'.join(tp for tp in valid_targets)}]")


################################ read_program_usage() ################################
def read_program_usage_message() -> str:
    fullpath = "README.md"
    try:
        with open(fullpath, "r") as fd:
            return fd.read()
    except FileNotFoundError as err:
        raise SystemExit(f"ERROR: {read_program_usage_message.__name__}() catches {err.__class__.__name__} exception => '{fullpath}'")


PROGRAM_DESCRIPTION = read_program_usage_message()
