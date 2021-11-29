######################################################
#
# Author: Davide Colombo
# Date: 21/11/21 16:19
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List
import airquality.logger.util.decorator as log_decorator
import airquality.database.op.ins.base as base
import airquality.database.rec.info as rec
import airquality.database.conn.adapt as db
import airquality.database.util.query as qry
import airquality.types.apiresp.inforesp as resp


class InfoInsertWrapper(base.InsertWrapper):

    def __init__(
            self, conn: db.DatabaseAdapter, builder: qry.QueryBuilder, record_builder: rec.InfoRecordBuilder, log_filename="log"
    ):
        super(InfoInsertWrapper, self).__init__(
            conn=conn, builder=builder, record_builder=record_builder, log_filename=log_filename)
        self.record_builder = record_builder
        self.start_sensor_id = None

    @log_decorator.log_decorator()
    def with_start_insert_sensor_id(self, sensor_id: int):
        self.start_sensor_id = sensor_id
        return self

    @log_decorator.log_decorator()
    def insert(self, api_responses: List[resp.SensorInfoResponse]) -> None:
        start_sensor_id = self.start_sensor_id
        sensor_values, api_param_values, geolocation_values = self.get_sensor_info_values(api_responses)
        query = self.query_builder.build_initialize_sensor_query(
            sensor_values=sensor_values,
            api_param_values=api_param_values,
            geolocation_values=geolocation_values
        )
        self.database_conn.send(query)
        self.log_report(start_id=start_sensor_id, api_responses=api_responses)

    @log_decorator.log_decorator()
    def get_sensor_info_values(self, api_responses: List[resp.SensorInfoResponse]):
        sensor_values = ""
        api_param_values = ""
        geolocation_values = ""

        for r in api_responses:
            self.record_builder.with_sensor_id(self.start_sensor_id)
            sensor_values += self.record_builder.get_sensor_value(sensor_name=r.sensor_name, sensor_type=r.sensor_type)

            for c in r.channels:
                api_param_values += self.record_builder.get_channel_param_value(
                        ident=c.ch_id, key=c.ch_key, name=c.ch_name, timest=c.last_acquisition
                    ) + ','

            geolocation_values += self.record_builder.get_geolocation_value(
                timest=r.geolocation.timestamp, geometry=r.geolocation.geometry
            )
            self.start_sensor_id += 1
        return sensor_values.strip(','), api_param_values.strip(','), geolocation_values.strip(',')

    @log_decorator.log_decorator()
    def log_report(self, start_id: int, api_responses: List[resp.SensorInfoResponse]):
        n = len(api_responses)
        self.log_info(f"{InfoInsertWrapper.__name__}: inserted {n}/{n} new sensors within sensor_id range "
                      f"[{start_id} - {start_id+n}]")
        for r in api_responses:
            self.log_info(f"{InfoInsertWrapper.__name__}: inserted {r.sensor_name}")
