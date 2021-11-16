######################################################
#
# Author: Davide Colombo
# Date: 14/11/21 21:58
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import List, Dict, Any
import airquality.database.operation.base as base
import airquality.database.util.conn as db
import airquality.database.util.query as query
import airquality.database.util.record.record as rec
import airquality.database.util.datatype.timestamp as ts


def get_insert_wrapper(sensor_type: str, conn: db.DatabaseAdapter, builder: query.QueryBuilder):
    if sensor_type == 'purpleair':
        return PurpleairInsertWrapper(conn=conn, query_builder=builder)
    elif sensor_type == 'atmotube':
        return AtmotubeInsertWrapper(conn=conn, query_builder=builder)
    elif sensor_type == 'thingspeak':
        return ThingspeakInsertWrapper(conn=conn, query_builder=builder)


class InsertWrapper(base.DatabaseOperationWrapper, abc.ABC):

    def __init__(self, conn: db.DatabaseAdapter, query_builder: query.QueryBuilder):
        super(InsertWrapper, self).__init__(conn=conn, query_builder=query_builder)
        self.sensor_record_builder = None
        self.sensor_location_record_builder = None
        self.api_param_record_builder = None
        self.sensor_info_record_builder = None
        self.mobile_record_builder = None
        self.station_record_builder = None

    def set_sensor_record_builder(self, builder: rec.SensorRecord):
        self.sensor_record_builder = builder

    def set_sensor_location_record_builder(self, builder: rec.SensorLocationRecord):
        self.sensor_location_record_builder = builder

    def set_sensor_info_record_builder(self, builder: rec.SensorInfoRecord):
        self.sensor_info_record_builder = builder

    def set_api_param_record_builder(self, builder: rec.APIParamRecord):
        self.api_param_record_builder = builder

    def set_mobile_record_builder(self, builder: rec.MobileMeasureRecord):
        self.mobile_record_builder = builder

    def set_station_record_builder(self, builder: rec.StationMeasureRecord):
        self.station_record_builder = builder

    @abc.abstractmethod
    def _exit_on_missing_external_dependencies(self):
        pass


################################ PURPLEAIR EXECUTOR CLASS ################################
class PurpleairInsertWrapper(InsertWrapper):

    def __init__(self, conn: db.DatabaseAdapter, query_builder: query.QueryBuilder):
        super(PurpleairInsertWrapper, self).__init__(conn=conn, query_builder=query_builder)

    ################################ METHOD FOR INITIALIZE SENSORS AND THEIR INFO ################################
    def initialize_sensors(self, sensor_data: List[Dict[str, Any]], start_id: int):

        self._exit_on_missing_external_dependencies()

        location_values = []
        api_param_values = []
        sensor_values = []
        sensor_info_values = []

        for data in sensor_data:
            sensor_values.append(self.sensor_record_builder.record(sensor_data=data))
            api_param_values.append(self.api_param_record_builder.record(sensor_data=data, sensor_id=start_id))
            location_values.append(self.sensor_location_record_builder.record(sensor_data=data, sensor_id=start_id))
            sensor_info_values.append(self.sensor_info_record_builder.record(sensor_data=data, sensor_id=start_id))
            self.info_messages.append(f"added sensor '{data['name']}' with id={start_id}")
            start_id += 1

        # Execute queries
        exec_query = self.builder.initialize_sensors(sensor_values=sensor_values, api_param_values=api_param_values,
                                                     location_values=location_values, sensor_info_values=sensor_info_values)
        self.conn.send(exec_query)

        # Log messages
        self.log_messages()

    ################################ METHOD FOR UPDATE LOCATIONS ################################
    def update_locations(self,
                         fetched_locations: List[Dict[str, Any]],
                         database_locations: Dict[str, Any],
                         name2id_map: Dict[str, Any]):

        self._exit_on_missing_external_dependencies()

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

    def _exit_on_missing_external_dependencies(self):
        err_msg_header = f"{InsertWrapper.__name__}: bad setup => missing external dependency "
        if self.sensor_info_record_builder is None:
            raise SystemExit(err_msg_header + f"'{rec.SensorInfoRecord.__name__}'")
        elif self.sensor_location_record_builder is None:
            raise SystemExit(err_msg_header + f"'{rec.SensorLocationRecord.__name__}'")
        elif self.api_param_record_builder is None:
            raise SystemExit(err_msg_header + f"'{rec.APIParamRecord.__name__}'")
        elif self.sensor_record_builder is None:
            raise SystemExit(err_msg_header + f"'{rec.SensorRecord.__name__}'")


################################ ATMOTUBE INSERT OPERATION CLASS ################################
class AtmotubeInsertWrapper(base.DatabaseOperationWrapper):

    def __init__(self, conn: db.DatabaseAdapter, query_builder: query.QueryBuilder):
        super(AtmotubeInsertWrapper, self).__init__(conn=conn, query_builder=query_builder)

    def insert_measurements(self, fetched_measurements: List[Dict[str, Any]], sensor_id: int, channel_name: str):
        measure_records = []
        for measure in fetched_measurements:
            measure_records.append(rec.MobileMeasureRecord(measure))

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
