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
        return purpleair.PurpleairEnvFact(path_to_env=path_to_env, command=command, target=target)
    elif target == 'atmotube':
        return atmotube.AtmotubeEnvFact(path_to_env=path_to_env, command=command, target=target)
    elif target == 'thingspeak':
        return thingspeak.ThingspeakEnvFact(path_to_env=path_to_env, command=command, target=target)
    elif target == 'geonames':
        return geonames.GeonamesEnvFact(path_to_env=path_to_env, command=command, target=target)
    else:
        raise SystemExit(f"WORK IN PROGRESS....")
