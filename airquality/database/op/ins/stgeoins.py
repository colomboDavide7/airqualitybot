######################################################
#
# Author: Davide Colombo
# Date: 21/11/21 16:50
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List
import airquality.logger.util.decorator as log_decorator
import airquality.database.op.ins.ins as base
import airquality.database.rec.stinforec as rec
import airquality.database.util.conn as connection
import airquality.database.util.query as query


class StationGeoInsertWrapper(base.InsertWrapper):

    def __init__(self, conn: connection.DatabaseAdapter, builder: query.QueryBuilder, log_filename="log"):
        super(StationGeoInsertWrapper, self).__init__(conn=conn, builder=builder, log_filename=log_filename)

    @log_decorator.log_decorator()
    def concat_location_query(self, records: List[rec.StationInfoRecord]) -> None:

        self.query_to_execute += self.query_builder.insert_locations(records)
        self.log_info(f"{StationGeoInsertWrapper.__name__}: inserted {len(records)}/{len(records)} new locations")

    @log_decorator.log_decorator()
    def concat_update_valid_to_timestamp(self, records: List[rec.StationInfoRecord]):
        self.query_to_execute += self.query_builder.update_valid_to_timestamp(records)
