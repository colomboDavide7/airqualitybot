######################################################
#
# Author: Davide Colombo
# Date: 11/11/21 13:00
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import sys
import airquality.app.application as app
import airquality.app.util.make as make
import airquality.app.util.args as arg


# Create error logger and debugger
error_logger = make.make_file_logger(file_path='log/errors.log')
debugger = make.make_console_debugger(use_color=True)


def get_application():

    # Check the usage and argument type
    bot_name, sensor_type = arg.exit_on_bad_commandline_arguments(sys.argv[1:])

    # Create the Application
    application = app.Application(bot_name=bot_name, sensor_type=sensor_type)

    # Set external dependencies
    application.set_debugger(debugger)

    return application


if __name__ == '__main__':

    try:
        app_obj = get_application()
        app_obj.setup()
        app_obj.log_messages()
        app_obj.run()
    except (SystemExit, AttributeError, KeyError) as ex:
        debugger.error(f"{ex!s}")
        error_logger.error(f"{ex!s}")
        sys.exit(1)
