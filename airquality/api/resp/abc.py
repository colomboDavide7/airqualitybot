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
import airquality.types.timestamp as tstype
import airquality.types.postgis as pgistype

ChannelParam = namedtuple('ChannelParam', ['key', 'ident', 'name'])
NameValue = namedtuple('NameValue', ['name', 'value'])


class APIRespTypeABC(abc.ABC):
    pass


# ------------------------------- InfoAPIRespTypeABC ------------------------------- #
class InfoAPIRespTypeABC(APIRespTypeABC, abc.ABC):

    @abc.abstractmethod
    def date_created(self) -> tstype.Timestamp:
        pass

    @abc.abstractmethod
    def sensor_type(self) -> str:
        pass

    @abc.abstractmethod
    def sensor_name(self) -> str:
        pass

    @abc.abstractmethod
    def geolocation(self) -> pgistype.PostgisGeometry:
        pass

    @abc.abstractmethod
    def channels(self) -> List[ChannelParam]:
        pass


# ------------------------------- MeasureAPIRespTypeABC ------------------------------- #
class MeasureAPIRespTypeABC(APIRespTypeABC, abc.ABC):

    @abc.abstractmethod
    def measures(self) -> List[NameValue]:
        pass

    @abc.abstractmethod
    def measured_at(self) -> tstype.Timestamp:
        pass

    @abc.abstractmethod
    def located_at(self) -> pgistype.PostgisGeometry:
        pass


# ------------------------------- APIRespBuilderABC ------------------------------- #
class APIRespBuilderABC(abc.ABC):

    @abc.abstractmethod
    def build(self, parsed_resp: Dict[str, Any]) -> List[APIRespTypeABC]:
        pass
