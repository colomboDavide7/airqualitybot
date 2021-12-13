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

    command, target = get_commandline_arguments(sys.argv[1:])
    env_fact = dispatcher.get_env_fact(path_to_env='.env', command=command, target=target)
    env = env_fact.craft_env()
    env.run()


################################ get_commandline_arguments() ################################
def get_commandline_arguments(args: List[str]) -> Tuple[str, str]:
    program_usage_msg = read_program_usage_message()
    validate_arguments(args=args, program_usage_msg=program_usage_msg)
    command, target = args
    validate_command(command=command, program_usage_msg=program_usage_msg)
    validate_target(target=target, program_usage_msg=program_usage_msg)

    return command, target


################################ validate_arguments() ################################
def validate_arguments(args: List[str], program_usage_msg: str) -> None:
    if not args:
        print(f"{validate_arguments.__name__}(): bad usage => missing required arguments.")
        print(program_usage_msg)
        sys.exit(1)
    if len(args) != 2:
        print(f"{validate_arguments.__name__}(): bad usage => wrong number of arguments.")
        print(program_usage_msg)
        sys.exit(1)


################################ validate_command() ################################
def validate_command(command: str, program_usage_msg: str) -> None:
    valid_commands = ["init", "update", "fetch"]
    if command not in valid_commands:
        print(f"{validate_command.__name__}: bad command => VALID COMMANDS: [{'|'.join(c for c in valid_commands)}]")
        print(program_usage_msg)
        sys.exit(1)


################################ validate_target() ################################
def validate_target(target: str, program_usage_msg: str) -> None:
    valid_targets = ["atmotube", "purpleair", "thingspeak", "geonames"]
    if target not in valid_targets:
        print(f"{validate_target.__name__}(): bad target => VALID TARGETS: [{'|'.join(tp for tp in valid_targets)}]")
        print(program_usage_msg)
        sys.exit(1)


################################ read_program_usage() ################################
def read_program_usage_message() -> str:
    fullpath = "README.md"
    try:
        with open(fullpath, "r") as fd:
            return fd.read()
    except FileNotFoundError:
        return "python(version) -m airquality command target"
