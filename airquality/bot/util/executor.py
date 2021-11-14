######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 14/11/21 16:12
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import List, Dict, Any
import airquality.database.conn as db
import airquality.database.util.sql.query as query


class QueryExecutor(abc.ABC):

    def __init__(self, conn: db.DatabaseAdapter, query_builder: query.QueryBuilder):
        self.conn = conn
        self.builder = query_builder


class BotQueryExecutor(QueryExecutor):

    def __init__(self, conn: db.DatabaseAdapter, query_builder: query.QueryBuilder, sensor_type: str):
        super(BotQueryExecutor, self).__init__(conn=conn, query_builder=query_builder)
        self.type = sensor_type

    def get_sensor_id(self) -> List[int]:
        exec_query = self.builder.select_sensor_ids_from_sensor_type(self.type)
        answer = self.conn.send(exec_query)
        return [t[0] for t in answer]

    def get_measure_param(self) -> Dict[str, Any]:
        exec_query = self.builder.select_measure_param_from_sensor_type(self.type)
        answer = self.conn.send(exec_query)
        return dict(answer)


class SensorQueryExecutor(QueryExecutor):

    def __init__(self, conn: db.DatabaseAdapter, query_builder: query.QueryBuilder):
        super(SensorQueryExecutor, self).__init__(conn=conn, query_builder=query_builder)

    def get_sensor_api_param(self, sensor_id: int) -> Dict[str, Any]:
        exec_query = self.builder.select_api_param_from_sensor_id(sensor_id)
        answer = self.conn.send(exec_query)
        return dict(answer)

    def get_last_acquisition(self, channel: str, sensor_id: int) -> str:
        exec_query = self.builder.select_last_acquisition(channel=channel, sensor_id=sensor_id)
        answer = self.conn.send(exec_query)
        unfolded = [str(t[0]) for t in answer]
        return unfolded[0]
