######################################################
#
# Author: Davide Colombo
# Date: 26/11/21 13:01
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import List
import airquality.database.op.sel.base as base
import airquality.database.util.conn as db
import airquality.database.util.query as qry
import airquality.types.channel as chtype


class MeasureDatabaseResponse:

    def __init__(self, sensor_id: int, api_param: List[chtype.Channel]):
        self.sensor_id = sensor_id
        self.api_param = api_param


class MeasureSelectWrapper(base.SelectWrapper, abc.ABC):

    def __init__(self, conn: db.DatabaseAdapter, builder: qry.QueryBuilder, sensor_type: str, log_filename="log"):
        super(MeasureSelectWrapper, self).__init__(conn=conn, builder=builder, log_filename=log_filename, sensor_type=sensor_type)

    def select(self) -> List[MeasureDatabaseResponse]:
        responses = []

        sensor_query = self.query_builder.select_sensor_id_from_type(type_=self.sensor_type)
        sensor_ids = self.database_conn.send(sensor_query)
        unfolded_sensor_ids = [t[0] for t in sensor_ids]
        for sensor_id in unfolded_sensor_ids:
            responses.append(
                MeasureDatabaseResponse(
                    sensor_id=sensor_id,
                    api_param=self._select_api_param(sensor_id=sensor_id)
                )
            )
        return responses

    @abc.abstractmethod
    def select_max_record_id(self) -> int:
        pass


class MobileMeasureSelectWrapper(MeasureSelectWrapper):

    def __init__(self, conn: db.DatabaseAdapter, builder: qry.QueryBuilder, sensor_type: str, log_filename="log"):
        super(MobileMeasureSelectWrapper, self).__init__(conn=conn, builder=builder, sensor_type=sensor_type, log_filename=log_filename)

    def select_max_record_id(self) -> int:
        exec_query = self.query_builder.select_max_mobile_record_id()
        response = self.database_conn.send(exec_query)
        max_record_id = response[0][0]
        return 1 if max_record_id is None else (max_record_id+1)


class StationMeasureSelectWrapper(MeasureSelectWrapper):

    def __init__(self, conn: db.DatabaseAdapter, builder: qry.QueryBuilder, sensor_type: str, log_filename="log"):
        super(StationMeasureSelectWrapper, self).__init__(conn=conn, builder=builder, sensor_type=sensor_type, log_filename=log_filename)

    def select_max_record_id(self) -> int:
        exec_query = self.query_builder.select_max_station_record_id()
        response = self.database_conn.send(exec_query)
        max_record_id = response[0][0]
        return 1 if max_record_id is None else (max_record_id+1)
