######################################################
#
# Author: Davide Colombo
# Date: 25/11/21 15:49
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List
import airquality.logger.util.decorator as log_decorator
import airquality.database.op.ins.ins as base
import airquality.database.rec.stmeasrec as rec
import airquality.database.util.conn as db
import airquality.database.util.query as qry


class StationMeasureInsertWrapper(base.InsertWrapper):

    def __init__(self, conn: db.DatabaseAdapter, query_builder: qry.QueryBuilder, log_filename="log"):
        super(StationMeasureInsertWrapper, self).__init__(conn=conn, query_builder=query_builder, log_filename=log_filename)

    @log_decorator.log_decorator()
    def concat_insert_station_measurements_query(self, records: List[rec.StationMeasureRecord]) -> None:

        self.query_to_execute += self.builder.insert_station_measurements(records=records)
        self.log_info(f"{StationMeasureInsertWrapper.__name__}: inserted {len(records)}/{len(records)} mobile records "
                      f"within record_id [{records[0].rec_id} - {records[-1].rec_id}]")

    @log_decorator.log_decorator()
    def concat_update_last_acquisition_timestamp_query(self, sensor_id: int, channel_name: str, last_acquisition: str) -> None:
        self.query_to_execute += self.builder.update_last_acquisition(
            sensor_id=sensor_id, channel_name=channel_name, last_timestamp=last_acquisition
        )
