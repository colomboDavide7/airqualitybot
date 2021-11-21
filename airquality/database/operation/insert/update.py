######################################################
#
# Author: Davide Colombo
# Date: 21/11/21 16:50
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List, Dict, Any
import airquality.adapter.config as adapt_const
import airquality.database.operation.insert.insert as base
import airquality.database.util.conn as connection
import airquality.database.util.query as query
import airquality.database.util.record.record as rec


class UpdateInsertWrapper(base.InsertWrapper):

    ################################ __init__ ################################
    def __init__(self,
                 conn: connection.DatabaseAdapter,
                 query_builder: query.QueryBuilder,
                 sensor_location_rec: rec.SensorLocationRecord,
                 log_filename="log"
    ):
        super(UpdateInsertWrapper, self).__init__(conn=conn, query_builder=query_builder, log_filename=log_filename)
        self.sensor_location_rec = sensor_location_rec
        self.name_to_id_map = None

    ################################ set_name_to_id_map ################################
    def set_name_to_id_map(self, mapping: Dict[str, Any]):
        self.name_to_id_map = mapping

    ################################ insert ################################
    def insert(self, sensor_data: List[Dict[str, Any]], sensor_id: int = None, sensor_channel: str = None):

        location_values = []
        for data in sensor_data:
            sensor_id = self.name_to_id_map[data[adapt_const.SENS_NAME]]
            location_values.append(self.sensor_location_rec.record(sensor_data=data, sensor_id=sensor_id))
            self.log_info(f"{UpdateInsertWrapper.__name__}: "
                          f"updated location for sensor '{data[adapt_const.SENS_NAME]}' with sensor_id={sensor_id}")

        # Build query to execute
        exec_query = self.query_builder.update_locations(location_values)
        # Execute query
        self.conn.send(exec_query)
