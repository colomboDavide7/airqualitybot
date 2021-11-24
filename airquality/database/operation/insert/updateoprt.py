######################################################
#
# Author: Davide Colombo
# Date: 21/11/21 16:50
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List
import airquality.database.operation.insert.insertoprt as base
import airquality.database.record.updtrec as updtrec
import airquality.database.util.conn as connection
import airquality.database.util.query as query


class UpdateInsertWrapper(base.InsertWrapper):

    def __init__(self, conn: connection.DatabaseAdapter, query_builder: query.QueryBuilder, log_filename="log"):
        super(UpdateInsertWrapper, self).__init__(conn=conn, query_builder=query_builder, log_filename=log_filename)

    def insert(self, records: List[updtrec.UpdateRecord]) -> None:

        update_info = []
        sensor_at_loc_values = ""

        for record in records:
            update_info.append(record.update_info)
            sensor_at_loc_values += record.sensor_at_loc_values

        exec_query = self.query_builder.update_locations(
            sensor_at_loc_values=sensor_at_loc_values,
            update_info=update_info
        )
        self.conn.send(exec_query)
        self.log_info(f"{UpdateInsertWrapper.__name__}: successfully insert all the records and updated all the locations")
