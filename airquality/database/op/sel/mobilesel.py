######################################################
#
# Author: Davide Colombo
# Date: 24/11/21 14:25
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List
import airquality.database.op.sel.sel as sel
import airquality.database.util.conn as connection
import airquality.database.util.query as query


class MobileDBResponse(sel.BaseDBResponse):

    def __init__(self, sensor_id: int, api_param: List[sel.ChannelParam], measure_param: List[sel.ParamNameID]):
        self.sensor_id = sensor_id
        self.api_param = api_param
        self.measure_param = measure_param


class MobileSelectWrapper(sel.SelectWrapper):

    def __init__(self, conn: connection.DatabaseAdapter, query_builder: query.QueryBuilder, sensor_type: str, log_filename="log"):
        super(MobileSelectWrapper, self).__init__(conn=conn, query_builder=query_builder, sensor_type=sensor_type, log_filename=log_filename)

    def select(self) -> List[MobileDBResponse]:
        responses = []

        sensor_query = self.builder.select_sensor_id_from_type(type_=self.sensor_type)
        sensor_ids = self.conn.send(sensor_query)
        for sensor_id in sensor_ids:
            api_param = self._select_api_param(sensor_id=sensor_id)
            measure_param = self._select_measure_param()
            responses.append(
                MobileDBResponse(sensor_id=sensor_id, api_param=api_param, measure_param=measure_param)
            )
        return responses
