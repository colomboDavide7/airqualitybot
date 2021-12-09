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
import airquality.file.util.loader as fileloader
import airquality.command.getfact as cmdfact
import airquality.database.conn.fact as dbfact
import airquality.database.conn.shutdown as dbshutdown


# Create error logger and debugger
error_logger = log.get_file_logger(file_path='log/errors.log', logger_name="errors")
console_logger = log.get_console_logger(use_color=True)


def main():
    try:
        command_name, command_type = get_commandline_arguments(sys.argv[1:])

        # ----------- GET COMMAND FACTORY CLASS -----------
        command_factory_cls = cmdfact.get_command_factory_cls(command_name=command_name, command_type=command_type)

        log_filename = command_type
        logger_file_path = f"log/{command_name}/{log_filename}.log"
        logger_name = f"{command_type}_{command_name}_logger"
        file_logger = log.get_file_logger(file_path=logger_file_path, logger_name=logger_name)

        # ----------- CREATE COMMAND's COMMON OBJECTS -----------
        connection, query_file_path = fileloader.load_environment_file()
        query_file = fileloader.load_structured_file(file_path=query_file_path, log_filename=log_filename)
        db_adapter = dbfact.get_database_adapter(connection_string=connection, log_filename=log_filename)
        db_adapter.open_conn()

        # ----------- COMMAND FACTORY -----------
        command_factory = command_factory_cls(query_file=query_file, db_adapt=db_adapter, log_filename=log_filename)
        command_factory.set_file_logger(logger=file_logger)
        command_factory.set_console_logger(logger=console_logger)

        # ----------- GET COMMAND OBJECT -----------
        commands2execute = command_factory.get_commands_to_execute(command_type=command_type)
        for command in commands2execute:
            command.execute()

        # ----------- SAFE SHUTDOWN -----------
        safe_shutdown()

    except (SystemExit, AttributeError, KeyError) as ex:
        console_logger.error(f"{ex!s}")
        error_logger.error(f"{ex!s}")
        sys.exit(1)
    finally:
        safe_shutdown()


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


################################ safe_shutdown() ################################
def safe_shutdown():
    dbshutdown.shutdown()
    log.logging.shutdown()
