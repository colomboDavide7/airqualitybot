######################################################
#
# Author: Davide Colombo
# Date: 24/11/21 14:26
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import List
import airquality.database.op.baseop as baseop
import airquality.database.util.conn as connection
import airquality.database.util.query as query
import airquality.database.dtype.timestamp as ts


class ParamNameValue:

    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value


class ParamNameTimestamp:

    def __init__(self, name: str, timestamp: ts.SQLTimestamp):
        self.name = name
        self.timestamp = timestamp


class Channel:

    def __init__(self, api_param: ParamNameValue, channel_info: ParamNameTimestamp):
        self.api_param = api_param
        self.channel_info = channel_info


def make_channels(api_param: List[ParamNameValue], channel_info: List[ParamNameTimestamp]) -> List[Channel]:
    channels = []
    for p in api_param:
        for c in channel_info:
            if p.name == c.name:
                channels.append(Channel(api_param=p, channel_info=c))
    return channels


class BaseDBResponse(abc.ABC):
    pass


class SelectWrapper(baseop.DatabaseWrapper, abc.ABC):

    def __init__(self, conn: connection.DatabaseAdapter, query_builder: query.QueryBuilder, sensor_type: str, log_filename="log"):
        super(SelectWrapper, self).__init__(conn=conn, query_builder=query_builder, log_filename=log_filename)
        self.sensor_type = sensor_type

    @abc.abstractmethod
    def select(self) -> List[BaseDBResponse]:
        pass
