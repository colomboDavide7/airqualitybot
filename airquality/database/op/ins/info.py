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


class StationInfoInsertWrapper(base.InsertWrapper):

    def __init__(self, conn: db.DatabaseAdapter, builder: qry.QueryBuilder, log_filename="log"):
        super(StationInfoInsertWrapper, self).__init__(conn=conn, builder=builder, log_filename=log_filename)

    @log_decorator.log_decorator()
    def concat_initialize_sensor_query(self, records: List[rec.SensorInfoRecord]) -> None:

        self.query_to_execute += self.query_builder.build_initialize_sensor_query(
            sensor_values=','.join(f"{r.get_sensor_value()}" for r in records),
            api_param_values=','.join(f"{r.get_channel_param_value()}" for r in records),
            geolocation_values=','.join(f"{r.get_geolocation_value()}" for r in records)
        )
        self.log_info(f"{StationInfoInsertWrapper.__name__}: inserted {len(records)}/{len(records)} new sensors")
