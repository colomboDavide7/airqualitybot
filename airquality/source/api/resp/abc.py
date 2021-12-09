######################################################
#
# Author: Davide Colombo
# Date: 26/11/21 08:51
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from collections import namedtuple
from typing import Dict, Any, List

ChannelParam = namedtuple('ChannelParam', ['key', 'ident', 'name'])
SensorGeolocation = namedtuple('SensorGeolocation', ['latitude', 'longitude'])
SensorInfo = namedtuple('SensorInfo', ['name', 'type'])
NameValue = namedtuple('NameValue', ['name', 'value'])


class APIRespTypeABC(abc.ABC):
    pass


class APIRespBuilderABC(abc.ABC):

    @abc.abstractmethod
    def build(self, parsed_resp: Dict[str, Any]) -> List[APIRespTypeABC]:
        pass
