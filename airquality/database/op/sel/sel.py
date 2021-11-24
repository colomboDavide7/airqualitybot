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


class ParamNameID:

    def __init__(self, id_: int, name: str):
        self.id = id_
        self.name = name


class ChannelParam:

    def __init__(self, id_: str, key: str, name: str, timestamp: ts.SQLTimestamp):
        self.id = id_
        self.key = key
        self.name = name
        self.last_acquisition = timestamp


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
    def _select_api_param(self, sensor_id: int) -> List[ChannelParam]:
        api_param_query = self.builder.select_api_param_from_sensor_id(sensor_id=sensor_id)
        api_param_resp = self.conn.send(api_param_query)

        api_param = []
        for ch_key, ch_id, ch_name, last_acquisition in api_param_resp:
            api_param.append(ChannelParam(id_=ch_id, key=ch_key, name=ch_name, timestamp=last_acquisition))
        return api_param

    def _select_measure_param(self) -> List[ParamNameID]:
        meas_param_query = self.builder.select_measure_param_from_sensor_type(sensor_type=self.sensor_type)
        measure_param_resp = self.conn.send(meas_param_query)
        measure_param = []
        for param_code, param_id in measure_param_resp:
            measure_param.append(ParamNameID(id_=param_id, name=param_code))
        return measure_param
