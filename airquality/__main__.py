######################################################
#
# Author: Davide Colombo
# Date: 11/11/21 13:00
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import sys
from typing import List, Tuple
import airquality.app.application as app
import airquality.logger.util.log as log


# Create error logger and debugger
error_logger = log.get_file_logger(file_path='log/errors.log', logger_name="errors")
console_logger = log.get_console_logger(use_color=True)


def main():
    try:
        app_obj = get_application()
        app_obj.setup()
        app_obj.run()
    except (SystemExit, AttributeError, KeyError) as ex:
        console_logger.error(f"{ex!s}")
        error_logger.error(f"{ex!s}")
        sys.exit(1)


def get_application():

    # Get arguments and create the Application
    bot_name, sensor_type = get_commandline_arguments(sys.argv[1:])
    application = app.Application(bot_name=bot_name, sensor_type=sensor_type)

    # Set external dependencies
    file_logger = log.get_file_logger(file_path=f'log/{bot_name}.log', mode='a+', logger_name=bot_name)
    application.set_file_logger(file_logger)
    application.set_console_logger(console_logger)

    return application


def get_commandline_arguments(args: List[str]) -> Tuple[str, str]:

    program_usage = "USAGE: python(version) -m airquality bot_name sensor_type"
    valid_combination = [('init', 'purpleair'), ('update', 'purpleair'), ('fetch', 'atmotube'), ('fetch', 'thingspeak')]

    if not args:
        raise SystemExit(f"'{get_commandline_arguments.__name__}()': bad usage => missing required arguments. {program_usage}")
    if len(args) != 2:
        raise SystemExit(f"'{get_commandline_arguments.__name__}()': bad usage => wrong number of argument, "
                         f"required 2, got {len(args)}. {program_usage}")

    bot_name = args[0]
    sensor_type = args[1]
    if (bot_name, sensor_type) not in valid_combination:
        raise SystemExit(f"'{get_commandline_arguments.__name__}():' bad arguments => '{sensor_type}' sensor type is "
                         f" not valid for '{bot_name}' bot. Valid combinations are: {valid_combination}")
    return bot_name, sensor_type


if __name__ == '__main__':
    main()
