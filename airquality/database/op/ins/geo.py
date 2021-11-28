######################################################
#
# Author: Davide Colombo
# Date: 21/11/21 16:50
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List
import airquality.logger.util.decorator as log_decorator
import airquality.database.op.ins.base as base
import airquality.database.rec.info as rec
import airquality.database.conn.adapt as db
import airquality.database.util.query as query


class StationGeoInsertWrapper(base.InsertWrapper):

    def __init__(self, conn: db.DatabaseAdapter, builder: query.QueryBuilder, log_filename="log"):
        super(StationGeoInsertWrapper, self).__init__(conn=conn, builder=builder, log_filename=log_filename)

    @log_decorator.log_decorator()
    def concat_location_query(self, records: List[rec.SensorInfoRecord]) -> None:

        self.query_to_execute += self.query_builder.build_insert_sensor_location_query(
            geolocation_values=','.join(f"{r.get_geolocation_value()}" for r in records)
        )
        self.log_info(f"{StationGeoInsertWrapper.__name__}: inserted {len(records)}/{len(records)} new locations")

    @log_decorator.log_decorator()
    def concat_update_valid_to_timestamp(self, records: List[rec.SensorInfoRecord]):
        for r in records:
            self.query_to_execute += self.query_builder.build_update_location_validity_query(
                valid_to=r.response.geolocation.timestamp.get_formatted_timestamp(),
                sensor_id=r.sensor_id
            )
