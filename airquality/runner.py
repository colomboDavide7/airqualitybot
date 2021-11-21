######################################################
#
# Author: Davide Colombo
# Date: 21/11/21 10:43
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import sys
from typing import List, Tuple
import airquality.logger.util.log as log
import airquality.command.init.setup as init_setup
import airquality.command.update.setup as upd_setup
import airquality.command.fetch.setup as ftc_setup


# Create error logger and debugger
error_logger = log.get_file_logger(file_path='log/errors.log', logger_name="errors")
console_logger = log.get_console_logger(use_color=True)


def main():
    try:
        cmd_name, sensor_type = get_commandline_arguments(sys.argv[1:])

        setup_obj = None
        logger_file_path = None
        logger_name = None

        if cmd_name == 'init':
            setup_obj = init_setup.PurpleairInitSetup(log_filename="purpleair")
            logger_file_path = "log/init/purpleair.log"
            logger_name = "purpleair_init"
        elif cmd_name == 'update':
            setup_obj = upd_setup.PurpleairUpdateSetup(log_filename="purpleair")
            logger_file_path = "log/update/purpleair.log"
            logger_name = "purpleair_update"
        elif cmd_name == 'fetch':
            if sensor_type == 'atmotube':
                setup_obj = ftc_setup.AtmotubeFetchSetup(log_filename="atmotube")
                logger_file_path = "log/fetch/atmotube.log"
                logger_name = "atmotube_fetch"
            elif sensor_type == "thingspeak":
                print("Thingspeak Fetch")
            else:
                raise SystemExit(f"{main.__name__}: bad sensor type '{sensor_type}' for command '{cmd_name}'")
        else:
            raise SystemExit(f"{main.__name__}: bad command '{cmd_name}'")

        setup_obj.set_file_logger(logger=log.get_file_logger(file_path=logger_file_path, logger_name=logger_name))
        setup_obj.set_console_logger(logger=console_logger)
        cmd_obj = setup_obj.setup(sensor_type=sensor_type)
        cmd_obj.execute()

    except (SystemExit, AttributeError, KeyError) as ex:
        console_logger.error(f"{ex!s}")
        error_logger.error(f"{ex!s}")
        sys.exit(1)


def get_commandline_arguments(args: List[str]) -> Tuple[str, str]:

    program_usage = "USAGE: python(version) -m airquality command_name sensor_type"
    valid_combination = [('init', 'purpleair'), ('update', 'purpleair'), ('fetch', 'atmotube'), ('fetch', 'thingspeak')]

    if not args:
        raise SystemExit(f"'{get_commandline_arguments.__name__}()': bad usage => missing required arguments. {program_usage}")
    if len(args) != 2:
        raise SystemExit(f"'{get_commandline_arguments.__name__}()': bad usage => wrong number of argument, "
                         f"required 2, got {len(args)}. {program_usage}")

    command_name = args[0]
    sensor_type = args[1]
    return command_name, sensor_type
