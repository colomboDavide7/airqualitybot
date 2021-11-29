######################################################
#
# Author: Davide Colombo
# Date: 21/11/21 16:50
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List, Dict, Any
import airquality.logger.util.decorator as log_decorator
import airquality.database.op.ins.base as base
import airquality.database.rec.info as rec
import airquality.database.conn.adapt as db
import airquality.database.util.query as query
import airquality.types.apiresp.inforesp as resp


class GeoInsertWrapper(base.InsertWrapper):

    def __init__(
            self, conn: db.DatabaseAdapter, builder: query.QueryBuilder, record_builder: rec.InfoRecordBuilder, log_filename="log"
    ):
        super(GeoInsertWrapper, self).__init__(
            conn=conn, builder=builder, record_builder=record_builder, log_filename=log_filename)
        self.record_builder = record_builder
        self.name2id = None

    def with_sensor_name2id(self, name2id: Dict[str, Any]):
        self.name2id = name2id
        return self

    @log_decorator.log_decorator()
    def insert(self, api_responses: List[resp.SensorInfoResponse]) -> None:
        geolocation_values = self.get_geolocation_values(api_responses)
        exec_query = self.get_update_valid_to_timestamp_queries(api_responses)
        exec_query += self.query_builder.build_insert_sensor_location_query(geolocation_values)
        self.database_conn.send(exec_query)
        self.log_report(api_responses)

    @log_decorator.log_decorator()
    def get_geolocation_values(self, api_responses: List[resp.SensorInfoResponse]) -> str:
        geolocation_values = ""
        for r in api_responses:
            self.record_builder.with_sensor_id(self.name2id[r.sensor_name])
            geolocation_values += self.record_builder.get_geolocation_value(
                timest=r.geolocation.timestamp, geometry=r.geolocation.geometry
            )
        return geolocation_values.strip(',')

    @log_decorator.log_decorator()
    def get_update_valid_to_timestamp_queries(self, api_responses: List[resp.SensorInfoResponse]) -> str:
        update_query = ""
        for r in api_responses:
            update_query += self.query_builder.build_update_location_validity_query(
                valid_to=r.geolocation.timestamp.get_formatted_timestamp(), sensor_id=self.name2id[r.sensor_name]
            )
        return update_query

    @log_decorator.log_decorator()
    def log_report(self, api_responses: List[resp.SensorInfoResponse]):
        self.log_info(f"{GeoInsertWrapper.__name__}: updated {len(api_responses)}/{len(api_responses)} locations")
        for r in api_responses:
            self.log_info(f"{GeoInsertWrapper.__name__}: updated {r.sensor_name}")
