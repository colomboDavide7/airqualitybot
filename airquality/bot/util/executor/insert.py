######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 14/11/21 21:58
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.bot.util.executor.base as base
from typing import List, Dict, Any
import airquality.database.conn as db
import airquality.database.util.sql.query as query
import airquality.database.util.sql.record as rec
import airquality.database.util.datatype.timestamp as ts


################################ PURPLEAIR EXECUTOR CLASS ################################
class PurpleairInsertionQueryExecutor(base.QueryExecutor):

    def __init__(self, conn: db.DatabaseAdapter, query_builder: query.QueryBuilder, geom_builder_cls, timest_cls):
        super(PurpleairInsertionQueryExecutor, self).__init__(conn=conn, query_builder=query_builder)
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
        self.log_messages(logging_msg)

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
            self.log_messages(["all sensors have the same location => done"])
            return

        # Execute the queries
        exec_query = self.builder.update_locations(location_records)
        self.conn.send(exec_query)

        # Log messages
        self.log_messages(logging_msg)


################################ ATMOTUBE EXECUTOR CLASS ################################
class AtmotubeInsertionQueryExecutor(base.QueryExecutor):

    def __init__(self, conn: db.DatabaseAdapter, query_builder: query.QueryBuilder):
        super(AtmotubeInsertionQueryExecutor, self).__init__(conn=conn, query_builder=query_builder)

    def insert_measurements(self, fetched_measurements: List[Dict[str, Any]]):
        pass


################################ THINGSPEAK EXECUTOR CLASS ################################
class ThingspeakInsertionQueryExecutor(base.QueryExecutor):

    def __init__(self, conn: db.DatabaseAdapter, query_builder: query.QueryBuilder):
        super(ThingspeakInsertionQueryExecutor, self).__init__(conn=conn, query_builder=query_builder)

    def insert_measurements(self, fetched_measurements: List[Dict[str, Any]]):
        pass
