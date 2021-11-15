######################################################
#
# Author: Davide Colombo
# Date: 14/11/21 21:58
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any, List
import airquality.database.operation.base as base
import airquality.database.util.conn as db
import airquality.database.util.sql.query as query


################################ SELECT FROM SENSOR TYPE - DATABASE OPERATION ################################
class SensorTypeSelectWrapper(base.DatabaseOperationWrapper):

    def __init__(self, conn: db.DatabaseAdapter, query_builder: query.QueryBuilder, sensor_type: str):
        super(SensorTypeSelectWrapper, self).__init__(conn=conn, query_builder=query_builder)
        self.type = sensor_type

    def get_sensor_id(self) -> List[int]:
        exec_query = self.builder.select_sensor_ids_from_sensor_type(self.type)
        answer = self.conn.send(exec_query)
        return [t[0] for t in answer]

    def get_measure_param(self) -> Dict[str, Any]:
        exec_query = self.builder.select_measure_param_from_sensor_type(self.type)
        answer = self.conn.send(exec_query)
        return dict(answer)

    def get_sensor_names(self) -> List[str]:
        exec_query = self.builder.select_sensor_names_from_sensor_type(self.type)
        answer = self.conn.send(exec_query)
        unfolded = [t[0] for t in answer]
        if not unfolded:
            self.logger.warning(f"no sensor found for type={self.type}")
            self.debugger.warning(f"no sensor found for type={self.type}")
        return unfolded

    def get_active_locations(self) -> Dict[str, Any]:
        exec_query = self.builder.select_active_locations(self.type)
        answer = self.conn.send(exec_query)
        return dict(answer)

    def get_name_id_map(self) -> Dict[str, Any]:
        exec_query = self.builder.select_sensor_name_id_mapping_from_sensor_type(self.type)
        answer = self.conn.send(exec_query)
        return dict(answer)

    def get_max_sensor_id(self) -> int:
        exec_query = self.builder.select_max_sensor_id()
        answer = self.conn.send(exec_query)
        unfolded = [t[0] for t in answer]

        # Set the 'sensor_id' from where to start sensor insertion
        sensor_id = 1
        if unfolded[0] is not None:
            sensor_id = unfolded[0] + 1

        # Log messages
        self.info_messages.append(f"found database sensor_id={unfolded[0]} => new insertion starts at sensor_id={sensor_id!s}")
        self.log_messages()

        return sensor_id


################################ SELECT FROM SENSOR ID - DATABASE OPERATION ################################
class SensorIDSelectWrapper(base.DatabaseOperationWrapper):

    def __init__(self, conn: db.DatabaseAdapter, query_builder: query.QueryBuilder):
        super(SensorIDSelectWrapper, self).__init__(conn=conn, query_builder=query_builder)

    def get_sensor_api_param(self, sensor_id: int) -> Dict[str, Any]:
        exec_query = self.builder.select_api_param_from_sensor_id(sensor_id)
        answer = self.conn.send(exec_query)
        return dict(answer)

    def get_last_acquisition(self, channel: str, sensor_id: int) -> str:
        exec_query = self.builder.select_last_acquisition(channel=channel, sensor_id=sensor_id)
        answer = self.conn.send(exec_query)
        unfolded = [str(t[0]) for t in answer]

        self.info_messages.append(f"get last_acquisition timestamp for sensor_id={sensor_id} => '{unfolded[0]}'")
        self.log_messages()

        return unfolded[0]
