######################################################
#
# Author: Davide Colombo
# Date: 11/12/21 18:17
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.env.sensor.purpleair as purpleair
import airquality.env.sensor.atmotube as atmotube
import airquality.env.sensor.thingspeak as thingspeak
import airquality.env.service.geonames as geonames


################################ get_env_fact() ################################
def get_env_fact(path_to_env: str, command: str, target: str):

    if target == 'purpleair':
        if command in ('init', 'update'):
            return purpleair.PurpleairEnvFact(path_to_env=path_to_env, command=command, target=target)
    elif target == 'atmotube':
        if command in ('fetch', ):
            return atmotube.AtmotubeEnvFact(path_to_env=path_to_env, command=command, target=target)
    elif target == 'thingspeak':
        if command in ('fetch', ):
            return thingspeak.ThingspeakEnvFact(path_to_env=path_to_env, command=command, target=target)
    elif target == 'geonames':
        if command in ('init', ):
            return geonames.GeonamesEnvFact(path_to_env=path_to_env, command=command, target=target)

    raise SystemExit(f"{get_env_fact.__name__}(): bad usage => '{target}' target cannot be used on '{command}' command...")
