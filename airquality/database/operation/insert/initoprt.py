######################################################
#
# Author: Davide Colombo
# Date: 21/11/21 16:19
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.logger.util.decorator as log_decorator
import airquality.database.operation.insert.insertoprt as base
import airquality.database.record.initrec as initrec
import airquality.database.util.conn as connection
import airquality.database.util.query as query


class InitializeInsertWrapper(base.InsertWrapper):

    def __init__(self, conn: connection.DatabaseAdapter, query_builder: query.QueryBuilder, log_filename="log"):
        super(InitializeInsertWrapper, self).__init__(conn=conn, query_builder=query_builder, log_filename=log_filename)

    @log_decorator.log_decorator()
    def insert(self, sensor_record: initrec.InitRecord) -> None:

        exec_query = self.query_builder.initialize_sensors(
            sensor_values=sensor_record.sensor_value,
            api_param_values=sensor_record.api_param_values,
            channel_info_values=sensor_record.channel_info_values,
            sensor_at_loc_values=sensor_record.sensor_at_loc_values
        )
        self.conn.send(exec_query)
        self.log_info(f"{InitializeInsertWrapper.__name__}: successfully inserted all the records")
