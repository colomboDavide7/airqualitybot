######################################################
#
# Author: Davide Colombo
# Date: 15/11/21 08:41
# Description: INSERT HERE THE DESCRIPTION
#
######################################################


def exit_on_bad_commandline_arguments(bot_name: str, sensor_type: str):
    """Function that raises SystemExit if the combination of the two command line arguments is invalid."""

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
