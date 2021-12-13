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
        print(read_program_usage_message())
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
        print(f"{validate_arguments.__name__}(): bad usage => missing required arguments.")
        sys.exit(1)
    if len(args) != 2:
        print(f"{validate_arguments.__name__}(): bad usage => wrong number of arguments.")
        sys.exit(1)


################################ validate_command() ################################
def validate_command(command: str) -> None:
    valid_commands = ["init", "update", "fetch"]
    if command not in valid_commands:
        print(f"{validate_command.__name__}: bad command => VALID COMMANDS: [{'|'.join(c for c in valid_commands)}]")
        sys.exit(1)


################################ validate_target() ################################
def validate_target(target: str) -> None:
    valid_targets = ["atmotube", "purpleair", "thingspeak", "geonames"]
    if target not in valid_targets:
        print(f"{validate_target.__name__}(): bad target => VALID TARGETS: [{'|'.join(tp for tp in valid_targets)}]")
        sys.exit(1)


################################ read_program_usage() ################################
def read_program_usage_message() -> str:
    fullpath = "README.md"
    try:
        with open(fullpath, "r") as fd:
            return fd.read()
    except FileNotFoundError:
        return "python(version) -m airquality command target"
