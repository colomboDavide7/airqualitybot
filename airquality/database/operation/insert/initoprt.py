######################################################
#
# Author: Davide Colombo
# Date: 21/11/21 16:19
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List
import airquality.logger.util.decorator as log_decorator
import airquality.database.operation.insert.insertoprt as base
import airquality.database.record.initrec as initrec
import airquality.database.util.conn as connection
import airquality.database.util.query as query


class InitInsertWrapper(base.InsertWrapper):

    def __init__(self, conn: connection.DatabaseAdapter, query_builder: query.QueryBuilder, log_filename="log"):
        super(InitInsertWrapper, self).__init__(conn=conn, query_builder=query_builder, log_filename=log_filename)

    @log_decorator.log_decorator()
    def insert(self, records: List[initrec.InitRecord]) -> None:

        sensor_values = ""
        api_param_values = ""
        channel_info_values = ""
        sensor_at_loc_values = ""

        for record in records:
            sensor_values += record.sensor_value
            api_param_values += record.api_param_value
            channel_info_values += record.channel_info_value
            sensor_at_loc_values += record.sensor_at_loc_value

        exec_query = self.query_builder.initialize_sensors(
            sensor_values=sensor_values,
            api_param_values=api_param_values,
            channel_info_values=channel_info_values,
            sensor_at_loc_values=sensor_at_loc_values
        )
        self.conn.send(exec_query)
        self.log_info(f"{InitInsertWrapper.__name__}: successfully inserted all the records")
