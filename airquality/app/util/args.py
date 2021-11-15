######################################################
#
# Author: Davide Colombo
# Date: 15/11/21 08:41
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import os
from typing import Dict, Any, List, Tuple

USAGE = "USAGE: python(version) -m airquality bot_name sensor_type"


def exit_on_bad_commandline_arguments(args: List[str]) -> Tuple[str, str]:
    """Function that raises SystemExit if the combination of the two command line arguments is invalid."""

    if not args:
        print(USAGE)
        raise SystemExit(f"'{exit_on_bad_commandline_arguments.__name__}()': bad usage => missing required arguments")

    if len(args) != 2:
        print(USAGE)
        raise SystemExit(f"'{exit_on_bad_commandline_arguments.__name__}()': bad usage => wrong number of argument, "
                         f"required 2, got {len(args)}")

    bot_name = args[0]
    sensor_type = args[1]

    err_msg = f"'{exit_on_bad_commandline_arguments.__name__}()': bad arguments => "
    raise_error = False
    if bot_name == 'init':
        if sensor_type not in ('purpleair',):
            err_msg += f"'{bot_name}' bot valid type is: ['purpleair']"
            raise_error = True

    elif bot_name == 'update':
        if sensor_type not in ('purpleair',):
            err_msg += f"'{bot_name}' bot valid type is: ['purpleair']"
            raise_error = True

    elif bot_name == 'fetch':
        if sensor_type not in ('atmotube', 'thingspeak',):
            err_msg += f"'{bot_name}' bot valid types are: ['atmotube', 'thingspeak']"
            raise_error = True

    if raise_error:
        raise SystemExit(err_msg)

    return bot_name, sensor_type


def exit_on_bad_api_param(url_param: Dict[str, Any], sensor_type: str):

    if sensor_type in ('atmotube', 'thingspeak'):
        if not url_param.get('format'):
            raise SystemExit(f"'{exit_on_bad_api_param.__name__}()': bad 'api.json' file structure => missing param='format'")


def exit_on_bad_env_param():

    if not os.environ.get('DBCONN'):
        raise SystemExit(f"'{exit_on_bad_env_param.__name__}()': bad '.env' file structure => missing 'DBCONN'")
    elif not os.environ.get('PURPLEAIR_KEY1'):
        raise SystemExit(f"'{exit_on_bad_env_param.__name__}()': bad '.env' file structure => missing 'PURPLEAIR_KEY1'")
