######################################################
#
# Author: Davide Colombo
# Date: 21/11/21 17:59
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List
import airquality.logger.util.decorator as log_decorator
import airquality.database.op.ins.ins as ins
import airquality.database.util.conn as db
import airquality.database.util.query as qry
import airquality.database.rec.mbmeasrec as mbrec


class MobileMeasureInsertWrapper(ins.InsertWrapper):

    def __init__(self, conn: db.DatabaseAdapter, builder: qry.QueryBuilder, log_filename="log"):
        super(MobileMeasureInsertWrapper, self).__init__(conn=conn, builder=builder, log_filename=log_filename)

    @log_decorator.log_decorator()
    def concat_mobile_measurements_query(self, records: List[mbrec.MobileMeasureRecord]) -> None:

        self.query_to_execute += self.query_builder.insert_mobile_measurements(records=records)
        self.log_info(f"{MobileMeasureInsertWrapper.__name__}: inserted {len(records)}/{len(records)} mobile records "
                      f"within record_id [{records[0].rec_id} - {records[-1].rec_id}]")

    @log_decorator.log_decorator()
    def concat_update_last_acquisition_timestamp_query(self, sensor_id: int, channel_name: str, last_acquisition: str) -> None:
        self.query_to_execute += self.query_builder.update_last_acquisition(
            sensor_id=sensor_id, channel_name=channel_name, last_timestamp=last_acquisition
        )
