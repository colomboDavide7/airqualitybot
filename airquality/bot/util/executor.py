######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 14/11/21 16:12
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import List, Dict, Any
import airquality.database.conn as db
import airquality.database.util.sql.query as query
import airquality.database.util.sql.record as rec
import airquality.database.util.datatype.timestamp as ts
import airquality.logger.log as log


class QueryExecutor(abc.ABC):

    def __init__(self, conn: db.DatabaseAdapter, query_builder: query.QueryBuilder):
        self.conn = conn
        self.builder = query_builder
        self.logger = None
        self.debugger = None

    def set_logger(self, logger: log.logging.Logger):
        self.logger = logger

    def set_debugger(self, debugger: log.logging.Logger):
        self.debugger = debugger


################################ BOT QUERY EXECUTOR ################################
class BotQueryExecutor(QueryExecutor):

    def __init__(self, conn: db.DatabaseAdapter, query_builder: query.QueryBuilder, sensor_type: str):
        super(BotQueryExecutor, self).__init__(conn=conn, query_builder=query_builder)
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
        return [t[0] for t in answer]

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
        sensor_id = 1
        if unfolded[0] is not None:
            sensor_id = unfolded[0] + 1

        msg = f"new insertion starts at sensor_id={sensor_id!s}"
        if self.debugger:
            self.debugger.info(msg)
        if self.logger:
            self.logger.info(msg)

        return sensor_id


################################ SENSOR QUERY EXECUTOR ################################
class SensorQueryExecutor(QueryExecutor):

    def __init__(self, conn: db.DatabaseAdapter, query_builder: query.QueryBuilder):
        super(SensorQueryExecutor, self).__init__(conn=conn, query_builder=query_builder)

    def get_sensor_api_param(self, sensor_id: int) -> Dict[str, Any]:
        exec_query = self.builder.select_api_param_from_sensor_id(sensor_id)
        answer = self.conn.send(exec_query)
        return dict(answer)

    def get_last_acquisition(self, channel: str, sensor_id: int) -> str:
        exec_query = self.builder.select_last_acquisition(channel=channel, sensor_id=sensor_id)
        answer = self.conn.send(exec_query)
        unfolded = [str(t[0]) for t in answer]
        return unfolded[0]


################################ PACKET QUERY EXECUTOR ################################
class PacketQueryExecutor(QueryExecutor):

    def __init__(self, conn: db.DatabaseAdapter, query_builder: query.QueryBuilder, geom_builder_cls, timest_cls):
        super(PacketQueryExecutor, self).__init__(conn=conn, query_builder=query_builder)
        self.geom_builder_class = geom_builder_cls
        self.timest_cls = timest_cls

    ################################ METHOD FOR INITIALIZE SENSORS AND THEIR INFO ################################
    def initialize_sensors(self, fetched_sensors: List[Dict[str, Any]], start_id: int):
        location_values = []
        api_param_values = []
        sensor_values = []
        sensor_info_values = []

        logging_msg = []
        for fetched_new_sensor in fetched_sensors:
            logging_msg.append(f"adding sensor '{fetched_new_sensor['name']}' with id={start_id}")
            # **************************
            sensor_value = rec.SensorRecord(sensor_id=start_id, packet=fetched_new_sensor)
            sensor_values.append(sensor_value)
            # **************************
            geometry = self.geom_builder_class(packet=fetched_new_sensor)
            valid_from = ts.CurrentTimestamp().ts
            geom = geometry.geom_from_text()
            geom_value = rec.LocationRecord(sensor_id=start_id, valid_from=valid_from, geom=geom)
            location_values.append(geom_value)
            # **************************
            api_param_value = rec.APIParamRecord(sensor_id=start_id, packet=fetched_new_sensor)
            api_param_values.append(api_param_value)
            # **************************
            sensor_info_value = rec.SensorInfoRecord(sensor_id=start_id, packet=fetched_new_sensor)
            sensor_info_value.add_timest_class(timest_cls=self.timest_cls)
            sensor_info_values.append(sensor_info_value)
            # **************************
            start_id += 1

        # Execute queries
        exec_query = self.builder.initialize_sensors(
            sensor_values=sensor_values,
            api_param_values=api_param_values,
            location_values=location_values,
            sensor_info_values=sensor_info_values
        )
        self.conn.send(exec_query)

        # Log messages
        if self.logger:
            for msg in logging_msg:
                self.logger.info(msg)
        # Debug messages
        if self.debugger:
            for msg in logging_msg:
                self.debugger.info(msg)

    ################################ METHOD FOR UPDATE LOCATIONS ################################
    def update_locations(self,
                         fetched_locations: List[Dict[str, Any]],
                         database_locations: Dict[str, Any],
                         name2id_map: Dict[str, Any]):

        location_records = []
        logging_msg = []
        for fetched_active_location in fetched_locations:
            name = fetched_active_location['name']
            geometry = self.geom_builder_class(fetched_active_location)
            # **************************
            if geometry.as_text() != database_locations[name]:
                logging_msg.append(f"found new location={geometry.as_text()} for name='{name}' => update location")
                # **************************
                sensor_id = name2id_map[name]
                geom = geometry.geom_from_text()
                valid_from = ts.CurrentTimestamp().ts
                # **************************
                record = rec.LocationRecord(sensor_id=sensor_id, valid_from=valid_from, geom=geom)
                location_records.append(record)

        # Log message when no location has been updated
        if not location_records:
            if self.logger:
                self.logger.warning("all sensor have the same location => done")
            if self.debugger:
                self.debugger.warning("all sensor have the same location => done")
            return

        # Execute the queries
        exec_query = self.builder.update_locations(location_records)
        self.conn.send(exec_query)

        # Log messages
        if self.logger:
            for msg in logging_msg:
                self.logger.info(msg)

        # Debug messages
        if self.debugger:
            for msg in logging_msg:
                self.debugger.info(msg)
