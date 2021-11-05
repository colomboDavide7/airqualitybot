######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 05/11/21 09:10
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from dataclasses import dataclass
from airquality.container.api_param_container import PurpleairAPIParamContainer
from airquality.container.geolocation_container import PurpleairGeolocationContainer
from airquality.container.sensor_container import PurpleairSensorContainer


@dataclass
class PurpleairContainer:
    sensor: PurpleairSensorContainer
    api_param: PurpleairAPIParamContainer
    geolocation: PurpleairGeolocationContainer
