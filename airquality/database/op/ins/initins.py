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
import airquality.database.rec.stinforec as rec
import airquality.database.util.conn as connection
import airquality.database.util.query as query


class InitInsertWrapper(base.InsertWrapper):

    def __init__(self, conn: connection.DatabaseAdapter, query_builder: query.QueryBuilder, log_filename="log"):
        super(InitInsertWrapper, self).__init__(conn=conn, query_builder=query_builder, log_filename=log_filename)

    @log_decorator.log_decorator()
    def insert(self, records: List[rec.StationInfoRecord]) -> None:

        sensor_values = ','.join(f"{r.get_sensor_value()}" for r in records)
        api_param_values = ','.join(f"{r.get_channel_param_value()}" for r in records)
        geolocation_values = ','.join(f"{r.get_geolocation_value()}" for r in records)

        exec_query = self.builder.initialize_sensors(
            sensor_values=sensor_values,
            api_param_values=api_param_values,
            geolocation_values=geolocation_values
        )
        self.conn.send(exec_query)
        self.log_info(f"{InitInsertWrapper.__name__}: successfully inserted all the records")
