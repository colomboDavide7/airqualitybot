######################################################
#
# Author: Davide Colombo
# Date: 11/12/21 18:17
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.env.sensor.purpleair as purpleair


def get_env_fact(path_to_env: str, command_name: str, command_type: str):

    if command_type == 'purpleair':
        return purpleair.PurpleairEnvFactory(path_to_env=path_to_env, command_name=command_name, command_type=command_type)
    else:
        raise SystemExit(f"WORK IN PROGRESS....")
