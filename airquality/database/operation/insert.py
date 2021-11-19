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
import airquality.adapter.config as c


def get_insert_wrapper(sensor_type: str, conn: db.DatabaseAdapter, builder: query.QueryBuilder):
    if sensor_type == 'purpleair':
        return PurpleairInsertWrapper(conn=conn, query_builder=builder)
    elif sensor_type == 'atmotube':
        return AtmotubeInsertWrapper(conn=conn, query_builder=builder)
    elif sensor_type == 'thingspeak':
        return ThingspeakInsertWrapper(conn=conn, query_builder=builder)
    else:
        raise SystemExit(f"'{get_insert_wrapper.__name__}():' bad type '{sensor_type}'")


################################ BASE CLASS FOR INSERT WRAPPER ################################
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


################################ PURPLEAIR INSERT WRAPPER CLASS ################################
class PurpleairInsertWrapper(InsertWrapper):

    def __init__(self, conn: db.DatabaseAdapter, query_builder: query.QueryBuilder):
        super(PurpleairInsertWrapper, self).__init__(conn=conn, query_builder=query_builder)

    ################################ METHOD FOR INITIALIZE SENSORS AND THEIR INFO ################################
    def initialize_sensors(self, sensor_data: List[Dict[str, Any]], start_id: int):

        self.log_info(f"{PurpleairInsertWrapper.__name__}: try to initialize sensors...")
        # Check external dependencies
        self._exit_on_missing_external_dependencies()

        location_values = []
        api_param_values = []
        sensor_values = []
        sensor_info_values = []
        # Build values to insert
        for data in sensor_data:
            sensor_values.append(self.sensor_record_builder.record(sensor_data=data))
            api_param_values.append(self.api_param_record_builder.record(sensor_data=data, sensor_id=start_id))
            location_values.append(self.sensor_location_record_builder.record(sensor_data=data, sensor_id=start_id))
            sensor_info_values.append(self.sensor_info_record_builder.record(sensor_data=data, sensor_id=start_id))
            self.log_info(f"{PurpleairInsertWrapper.__name__}: added sensor '{data[c.SENS_NAME]}' with id={start_id}")
            start_id += 1

        # Build query to execute
        exec_query = self.builder.initialize_sensors(sensor_values=sensor_values,
                                                     api_param_values=api_param_values,
                                                     location_values=location_values,
                                                     sensor_info_values=sensor_info_values)
        # Execute query
        self.conn.send(exec_query)
        # Log messages
        self.log_info(f"{PurpleairInsertWrapper.__name__}: done")

    ################################ METHOD FOR UPDATE LOCATIONS ################################
    def update_locations(self, changed_sensors: List[Dict[str, Any]], name2id_map: Dict[str, Any]):

        self.log_info(f"{PurpleairInsertWrapper.__name__}: try to update sensor locations...")
        # Check external dependency
        if self.sensor_location_record_builder is None:
            raise SystemExit(f"{PurpleairInsertWrapper.__name__}: bad setup => missing external dependency "
                             f"'{rec.SensorLocationRecord.__name__}'")
        # Build location values to insert
        location_values = []
        for data in changed_sensors:
            sensor_id = name2id_map[data[c.SENS_NAME]]
            location_values.append(self.sensor_location_record_builder.record(sensor_data=data, sensor_id=sensor_id))
            self.log_info(f"{PurpleairInsertWrapper.__name__}: "
                          f"updated location for sensor '{data[c.SENS_NAME]}' with sensor_id={sensor_id}")
        # Build query to execute
        exec_query = self.builder.update_locations(location_values)
        # Execute query
        self.conn.send(exec_query)
        # Log messages
        self.log_info(f"{PurpleairInsertWrapper.__name__}: done")

    def _exit_on_missing_external_dependencies(self):
        err_msg_header = f"{PurpleairInsertWrapper.__name__}: bad setup => missing external dependency "

        if self.sensor_info_record_builder is None:
            raise SystemExit(err_msg_header + f"'{rec.SensorInfoRecord.__name__}'")
        elif self.sensor_location_record_builder is None:
            raise SystemExit(err_msg_header + f"'{rec.SensorLocationRecord.__name__}'")
        elif self.api_param_record_builder is None:
            raise SystemExit(err_msg_header + f"'{rec.APIParamRecord.__name__}'")
        elif self.sensor_record_builder is None:
            raise SystemExit(err_msg_header + f"'{rec.SensorRecord.__name__}'")


################################ ATMOTUBE INSERT WRAPPER CLASS ################################
class AtmotubeInsertWrapper(InsertWrapper):

    def __init__(self, conn: db.DatabaseAdapter, query_builder: query.QueryBuilder):
        super(AtmotubeInsertWrapper, self).__init__(conn=conn, query_builder=query_builder)

    def insert_measurements(self, sensor_data: List[Dict[str, Any]], sensor_id: int, channel: str):

        self.log_info(f"{AtmotubeInsertWrapper.__name__}: try to insert new measurements...")
        # Check external dependencies
        self._exit_on_missing_external_dependencies()
        # Build values to insert
        measure_values = [self.mobile_record_builder.record(sensor_data=data) for data in sensor_data]
        # Build query to execute
        exec_query = self.builder.insert_mobile_measurements(values=measure_values, sensor_id=sensor_id, channel=channel)
        # Execute query
        self.conn.send(exec_query)
        # Log messages
        self._log_message(sensor_data=sensor_data)
        self.log_info(f"{AtmotubeInsertWrapper.__name__}: done")

    def _log_message(self, sensor_data: List[Dict[str, Any]]):
        first_measure_id = sensor_data[0][c.REC_ID]
        last_measure_id = sensor_data[-1][c.REC_ID]
        n_measure = (last_measure_id - first_measure_id) + 1
        self.log_info(f"...inserted {n_measure} mobile records within [{first_measure_id} - {last_measure_id}] record_id range...")

    def _exit_on_missing_external_dependencies(self):
        msg = f"{AtmotubeInsertWrapper.__name__}: bad setup => "

        if self.mobile_record_builder is None:
            raise SystemExit(f"{msg} missing external dependencies 'mobile_record_builder'")


################################ THINGSPEAK INSERT WRAPPER CLASS ################################
class ThingspeakInsertWrapper(InsertWrapper):

    def __init__(self, conn: db.DatabaseAdapter, query_builder: query.QueryBuilder):
        super(ThingspeakInsertWrapper, self).__init__(conn=conn, query_builder=query_builder)

    def insert_measurements(self, sensor_data: List[Dict[str, Any]], sensor_id: int, channel: str):

        self.log_info(f"{ThingspeakInsertWrapper.__name__}: try to insert new measurements...")
        # Check external dependencies
        self._exit_on_missing_external_dependencies()
        # Build values to insert
        measure_values = [self.station_record_builder.record(sensor_data=data, sensor_id=sensor_id) for data in sensor_data]
        # Build query to execute
        exec_query = self.builder.insert_station_measurements(values=measure_values, sensor_id=sensor_id, channel=channel)
        # Execute query
        self.conn.send(exec_query)
        # Log messages
        self._log_message(sensor_data=sensor_data)
        self.log_info(f"{ThingspeakInsertWrapper.__name__}: done")

    def _log_message(self, sensor_data: List[Dict[str, Any]]):
        first_measure_id = sensor_data[0][c.REC_ID]
        last_measure_id = sensor_data[-1][c.REC_ID]
        n_measure = (last_measure_id - first_measure_id) + 1
        self.log_info(f"...inserted {n_measure} mobile records within [{first_measure_id} - {last_measure_id}] record_id range...")

    def _exit_on_missing_external_dependencies(self):
        msg = f"{ThingspeakInsertWrapper.__name__}: bad setup =>"

        if self.station_record_builder is None:
            raise SystemExit(f"{msg} missing external dependency 'station_record_builder'")
