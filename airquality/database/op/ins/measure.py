######################################################
#
# Author: Davide Colombo
# Date: 26/11/21 12:38
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import List
import airquality.database.op.ins.base as base
import airquality.logger.util.decorator as log_decorator
import airquality.database.rec.measure as rec
import airquality.database.conn.adapt as db
import airquality.database.util.query as qry


class MeasureInsertWrapper(base.InsertWrapper, abc.ABC):

    def __init__(self, conn: db.DatabaseAdapter, builder: qry.QueryBuilder, log_filename="log"):
        super(MeasureInsertWrapper, self).__init__(conn=conn, builder=builder, log_filename=log_filename)

    @abc.abstractmethod
    def concat_measure_query(self, records: List[rec.MeasureRecord]) -> None:
        pass

    @log_decorator.log_decorator()
    def concat_update_last_acquisition_timestamp_query(self, sensor_id: int, channel_name: str, last_acquisition: str) -> None:
        self.query_to_execute += self.query_builder.build_update_last_channel_acquisition_query(
            sensor_id=sensor_id, channel_name=channel_name, last_timestamp=last_acquisition
        )


################################ MOBILE MEASURE INSERT WRAPPER ################################
class MobileMeasureInsertWrapper(MeasureInsertWrapper):

    def __init__(self, conn: db.DatabaseAdapter, builder: qry.QueryBuilder, log_filename="log"):
        super(MobileMeasureInsertWrapper, self).__init__(conn=conn, builder=builder, log_filename=log_filename)

    @log_decorator.log_decorator()
    def concat_measure_query(self, records: List[rec.MobileMeasureRecord]) -> None:

        self.query_to_execute += self.query_builder.build_insert_mobile_measure_query(
            mobile_measure_values=','.join(f"{r.get_measure_values()}" for r in records)
        )

        self.log_info(f"{MobileMeasureInsertWrapper.__name__}: inserted {len(records)}/{len(records)} mobile records "
                      f"within record_id [{records[0].record_id} - {records[-1].record_id}]")


################################ STATION MEASURE INSERT WRAPPER ################################
class StationMeasureInsertWrapper(MeasureInsertWrapper):

    def __init__(self, conn: db.DatabaseAdapter, builder: qry.QueryBuilder, log_filename="log"):
        super(StationMeasureInsertWrapper, self).__init__(conn=conn, builder=builder, log_filename=log_filename)

    @log_decorator.log_decorator()
    def concat_measure_query(self, records: List[rec.StationMeasureRecord]) -> None:

        self.query_to_execute += self.query_builder.build_insert_station_measure_query(
            station_measure_values=','.join(f"{r.get_measure_values()}" for r in records)
        )
        self.log_info(f"{StationMeasureInsertWrapper.__name__}: inserted {len(records)}/{len(records)} mobile records "
                      f"within record_id [{records[0].record_id} - {records[-1].record_id}]")
