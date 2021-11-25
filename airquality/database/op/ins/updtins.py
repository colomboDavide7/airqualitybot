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


class UpdateInsertWrapper(base.InsertWrapper):

    def __init__(self, conn: connection.DatabaseAdapter, query_builder: query.QueryBuilder, log_filename="log"):
        super(UpdateInsertWrapper, self).__init__(conn=conn, query_builder=query_builder, log_filename=log_filename)

    @log_decorator.log_decorator()
    def insert(self, records: List[rec.StationInfoRecord]) -> None:

        geolocation_values = ','.join(f"{r.get_geolocation_value()}" for r in records)

        exec_query = self.builder.update_locations(geolocation_values=geolocation_values, records=records)
        self.conn.send(exec_query)
        self.log_info(f"{UpdateInsertWrapper.__name__}: successfully insert all the records and updated all the locations")
