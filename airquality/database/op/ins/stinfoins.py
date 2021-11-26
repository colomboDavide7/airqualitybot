######################################################
#
# Author: Davide Colombo
# Date: 21/11/21 16:19
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List
import airquality.logger.util.decorator as log_decorator
import airquality.database.op.ins.ins as base
import airquality.database.rec.info as rec
import airquality.database.util.conn as db
import airquality.database.util.query as qry


class StationInfoInsertWrapper(base.InsertWrapper):

    def __init__(self, conn: db.DatabaseAdapter, builder: qry.QueryBuilder, log_filename="log"):
        super(StationInfoInsertWrapper, self).__init__(conn=conn, builder=builder, log_filename=log_filename)

    @log_decorator.log_decorator()
    def concat_initialize_sensor_query(self, records: List[rec.StationInfoRecord]) -> None:

        self.query_to_execute += self.query_builder.initialize_sensors(records=records)
        self.log_info(f"{StationInfoInsertWrapper.__name__}: inserted {len(records)}/{len(records)} new sensors")
