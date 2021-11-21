######################################################
#
# Author: Davide Colombo
# Date: 21/11/21 16:19
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List, Dict, Any
import airquality.adapter.config as adapt_const
import airquality.database.operation.insert.insert as base
import airquality.database.util.record.record as rec
import airquality.logger.util.decorator as log_decorator
import airquality.database.util.conn as connection
import airquality.database.util.query as query


class InitializeInsertWrapper(base.InsertWrapper):

    ################################ __init__ ################################
    def __init__(self, conn: connection.DatabaseAdapter,
                 query_builder: query.QueryBuilder,
                 sensor_rec: rec.SensorRecord,
                 sensor_api_rec: rec.APIParamRecord,
                 sensor_info_rec: rec.SensorInfoRecord,
                 sensor_location_rec: rec.SensorLocationRecord,
                 log_filename="log"
                 ):
        super(InitializeInsertWrapper, self).__init__(conn=conn, query_builder=query_builder, log_filename=log_filename)
        self.sensor_rec = sensor_rec
        self.sensor_api_rec = sensor_api_rec
        self.sensor_info_rec = sensor_info_rec
        self.sensor_location_rec = sensor_location_rec

    ################################ insert ################################
    @log_decorator.log_decorator()
    def insert(self, sensor_data: List[Dict[str, Any]], sensor_id: int = None, sensor_channel: str = None):
        location_values = []
        api_param_values = []
        sensor_values = []
        sensor_info_values = []

        # Build values to insert
        for data in sensor_data:
            # Append values
            sensor_values.append(self.sensor_rec.record(sensor_data=data))
            api_param_values.append(self.sensor_api_rec.record(sensor_data=data, sensor_id=sensor_id))
            location_values.append(self.sensor_location_rec.record(sensor_data=data, sensor_id=sensor_id))
            sensor_info_values.append(self.sensor_info_rec.record(sensor_data=data, sensor_id=sensor_id))

            # Log message
            self.log_info(
                f"{InitializeInsertWrapper.__name__}: added sensor '{data[adapt_const.SENS_NAME]}' with id={sensor_id}")

            # Increment sensor id
            sensor_id += 1

        # Build query to execute
        exec_query = self.query_builder.initialize_sensors(sensor_values=sensor_values,
                                                           api_param_values=api_param_values,
                                                           location_values=location_values,
                                                           sensor_info_values=sensor_info_values)
        self.conn.send(exec_query)
