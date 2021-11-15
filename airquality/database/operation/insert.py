######################################################
#
# Author: Davide Colombo
# Date: 14/11/21 21:58
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List, Dict, Any
import airquality.database.operation.base as base
import airquality.database.util.conn as db
import airquality.database.util.sql.query as query
import airquality.database.util.sql.record as rec
import airquality.database.util.datatype.timestamp as ts


def get_insert_wrapper(sensor_type: str, conn: db.DatabaseAdapter, builder: query.QueryBuilder):
    if sensor_type == 'purpleair':
        return PurpleairInsertWrapper(conn=conn, query_builder=builder)
    elif sensor_type == 'atmotube':
        return AtmotubeInsertWrapper(conn=conn, query_builder=builder)
    elif sensor_type == 'thingspeak':
        return ThingspeakInsertWrapper(conn=conn, query_builder=builder)


################################ PURPLEAIR EXECUTOR CLASS ################################
class PurpleairInsertWrapper(base.DatabaseOperationWrapper):

    def __init__(self, conn: db.DatabaseAdapter, query_builder: query.QueryBuilder):
        super(PurpleairInsertWrapper, self).__init__(conn=conn, query_builder=query_builder)

    ################################ METHOD FOR INITIALIZE SENSORS AND THEIR INFO ################################
    def initialize_sensors(self, sensor_data: List[Dict[str, Any]], start_id: int):

        location_values = []
        api_param_values = []
        sensor_values = []
        sensor_info_values = []

        for data in sensor_data:
            self.info_messages.append(f"adding sensor '{data['name']}' with id={start_id}")
            # **************************
            sensor_value = rec.SensorRecord(sensor_id=start_id, packet=data)
            sensor_values.append(sensor_value)
            # **************************
            valid_from = ts.CurrentTimestamp().ts
            geom = data['geom'].geom_from_text()
            geom_value = rec.LocationRecord(sensor_id=start_id, valid_from=valid_from, geom=geom)
            location_values.append(geom_value)
            # **************************
            api_param_value = rec.APIParamRecord(sensor_id=start_id, packet=data)
            api_param_values.append(api_param_value)
            # **************************
            sensor_info_value = rec.SensorInfoRecord(sensor_id=start_id, packet=data)
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
        self.log_messages()

    ################################ METHOD FOR UPDATE LOCATIONS ################################
    def update_locations(self,
                         fetched_locations: List[Dict[str, Any]],
                         database_locations: Dict[str, Any],
                         name2id_map: Dict[str, Any]):

        location_records = []
        for fetched_active_location in fetched_locations:
            name = fetched_active_location['name']
            geometry = fetched_active_location['geom']
            # **************************
            if geometry.as_text() != database_locations[name]:
                self.info_messages.append(
                    f"found new location={geometry.as_text()} for name='{name}' => update location")
                # **************************
                sensor_id = name2id_map[name]
                geom = geometry.geom_from_text()
                valid_from = ts.CurrentTimestamp().ts
                # **************************
                record = rec.LocationRecord(sensor_id=sensor_id, valid_from=valid_from, geom=geom)
                location_records.append(record)

        # Log message when no location has been updated
        if not location_records:
            self.warning_messages.append("all sensors have the same location => done")
            self.log_messages()
            return

        # Execute the queries
        exec_query = self.builder.update_locations(location_records)
        self.conn.send(exec_query)

        # Log messages
        self.log_messages()


################################ ATMOTUBE INSERT OPERATION CLASS ################################
class AtmotubeInsertWrapper(base.DatabaseOperationWrapper):

    def __init__(self, conn: db.DatabaseAdapter, query_builder: query.QueryBuilder):
        super(AtmotubeInsertWrapper, self).__init__(conn=conn, query_builder=query_builder)

    def insert_measurements(self,
                            fetched_measurements: List[Dict[str, Any]],
                            measure_param_map: Dict[str, Any],
                            sensor_id: int,
                            channel_name: str
                            ):
        measure_records = []
        for measure in fetched_measurements:
            record = rec.MobileMeasureRecord(packet=measure)
            record.set_measure_param_map(measure_param_map)
            measure_records.append(record)

        first_measure_id = fetched_measurements[0]['record_id']
        last_measure_id = fetched_measurements[-1]['record_id']
        self.info_messages.append(f"fetched measurements from id={first_measure_id} to id={last_measure_id}")
        self.log_messages()

        # Build the query for inserting all the measurements
        exec_query = self.builder.insert_mobile_measurements(
            values=measure_records,
            sensor_id=sensor_id,
            channel_name=channel_name
        )
        self.conn.send(exec_query)


################################ THINGSPEAK INSERT OPERATION CLASS ################################
class ThingspeakInsertWrapper(base.DatabaseOperationWrapper):

    def __init__(self, conn: db.DatabaseAdapter, query_builder: query.QueryBuilder):
        super(ThingspeakInsertWrapper, self).__init__(conn=conn, query_builder=query_builder)

    def insert_measurements(self,
                            fetched_measurements: List[Dict[str, Any]],
                            measure_param_map: Dict[str, Any],
                            sensor_id: int,
                            channel_name: str):
        measure_records = []
        for measure in fetched_measurements:
            record = rec.StationMeasureRecord(packet=measure, sensor_id=sensor_id)
            record.set_measure_param_map(measure_param_map)
            measure_records.append(record)

        first_measure_id = fetched_measurements[0]['record_id']
        last_measure_id = fetched_measurements[-1]['record_id']
        self.info_messages.append(f"fetched measurements from id={first_measure_id} to id={last_measure_id}")
        self.log_messages()

        # Build the query for inserting all the measurements
        exec_query = self.builder.insert_station_measurements(
            values=measure_records,
            sensor_id=sensor_id,
            channel_name=channel_name
        )
        self.conn.send(exec_query)
