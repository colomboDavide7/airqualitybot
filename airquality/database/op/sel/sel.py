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

    def select_max_sensor_id(self):
        sel_query = self.builder.select_max_sensor_id()
        response = self.conn.send(sel_query)
        max_id = response[0][0]
        return 1 if max_id is None else (max_id+1)

    @abc.abstractmethod
    def select(self) -> List[BaseDBResponse]:
        pass

    ################################ protected methods ################################
    def _select_api_param(self, sensor_id: int) -> List[ParamNameValue]:
        api_param_query = self.builder.select_api_param_from_sensor_id(sensor_id=sensor_id)
        api_param_resp = self.conn.send(api_param_query)

        api_param = []
        for param_name, param_value in api_param_resp:
            api_param.append(ParamNameValue(name=param_name, value=param_value))
        return api_param

    def _select_channel_info(self, sensor_id: int) -> List[ParamNameTimestamp]:
        channel_info_query = self.builder.select_channel_info_from_sensor_id(sensor_id=sensor_id)
        channel_info_resp = self.conn.send(channel_info_query)

        channel_info = []
        for channel_name, last_acquisition in channel_info_resp:
            channel_info.append(ParamNameTimestamp(name=channel_name, timestamp=last_acquisition))
        return channel_info
