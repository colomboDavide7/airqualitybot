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

    command_name, command_type = get_commandline_arguments(sys.argv[1:])
    env_fact = dispatcher.get_env_fact(path_to_env='.env', command_name=command_name, command_type=command_type)
    env = env_fact.craft_env()
    env.run()


################################ get_commandline_arguments() ################################
def get_commandline_arguments(args: List[str]) -> Tuple[str, str]:

    function_name = get_commandline_arguments.__name__
    program_usage = "USAGE: python(version) -m airquality command_name sensor_type"

    if not args:
        raise SystemExit(f"{function_name}(): bad usage => missing required arguments. {program_usage}")
    if len(args) != 2:
        raise SystemExit(f"{function_name}(): bad usage => wrong number of argument. {program_usage}")

    command_name = args[0]
    sensor_type = args[1]

    valid_commands = ["init", "update", "fetch"]
    if command_name not in valid_commands:
        raise SystemExit(f"{function_name}: bad command => VALID COMMANDS: [{'|'.join(c for c in valid_commands)}]")

    valid_types = ["atmotube", "purpleair", "thingspeak", "geonames"]
    if sensor_type not in valid_types:
        raise SystemExit(f"{function_name}(): bad type => VALID TYPES: [{'|'.join(tp for tp in valid_types)}]")

    return command_name, sensor_type
