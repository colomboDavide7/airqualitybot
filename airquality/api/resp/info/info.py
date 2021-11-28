######################################################
#
# Author: Davide Colombo
# Date: 26/11/21 11:09
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import List, Dict, Any
import airquality.api.resp.base as base
import airquality.types.geolocation as geotype
import airquality.types.channel as chtype


class InfoAPIRespBuilder(base.APIRespBuilder, abc.ABC):

    @abc.abstractmethod
    def get_sensor_name(self, item: Dict[str, Any]) -> str:
        pass

    @abc.abstractmethod
    def get_channels(self, item: Dict[str, Any]) -> List[chtype.Channel]:
        pass

    @abc.abstractmethod
    def get_geolocation(self, item: Dict[str, Any]) -> geotype.Geolocation:
        pass
