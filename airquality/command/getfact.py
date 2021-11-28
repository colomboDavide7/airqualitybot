######################################################
#
# Author: Davide Colombo
# Date: 28/11/21 18:04
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.command.fetch.fact as fetchfact
import airquality.command.init.fact as initfact
import airquality.command.update.fact as updtfact


def get_command_factory_cls(command_name: str, sensor_type: str):

    if command_name == 'init':
        return initfact.get_init_factory_cls(sensor_type=sensor_type)
    elif command_name == 'update':
        return updtfact.get_update_factory_cls(sensor_type=sensor_type)
    elif command_name == 'fetch':
        return fetchfact.get_fetch_factory_cls(sensor_type=sensor_type)
    else:
        raise SystemExit(f"{get_command_factory_cls.__name__}: command_name='{command_name}' does not exist")
