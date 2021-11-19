######################################################
#
# Author: Davide Colombo
# Date: 14/11/21 21:58
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import List, Dict, Any
import airquality.logger.util.decorator as log_decorator
import airquality.database.operation.base as base
import airquality.database.util.conn as db
import airquality.database.util.query as query
import airquality.database.util.record.record as rec
import airquality.adapter.config as adapt_const


def get_insert_wrapper(sensor_type: str, conn: db.DatabaseAdapter, builder: query.QueryBuilder, log_filename="app"):
    if sensor_type == 'purpleair':
        return PurpleairInsertWrapper(conn=conn, query_builder=builder, log_filename=log_filename)
    elif sensor_type == 'atmotube':
        return AtmotubeInsertWrapper(conn=conn, query_builder=builder, log_filename=log_filename)
    elif sensor_type == 'thingspeak':
        return ThingspeakInsertWrapper(conn=conn, query_builder=builder, log_filename=log_filename)
    else:
        raise SystemExit(f"'{get_insert_wrapper.__name__}():' bad type '{sensor_type}'")


################################ BASE CLASS FOR INSERT WRAPPER ################################
class InsertWrapper(base.DatabaseOperationWrapper, abc.ABC):

    def __init__(self, conn: db.DatabaseAdapter, query_builder: query.QueryBuilder, log_filename="app"):
        super(InsertWrapper, self).__init__(conn=conn, query_builder=query_builder, log_filename=log_filename)
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

    def __init__(self, conn: db.DatabaseAdapter, query_builder: query.QueryBuilder, log_filename="app"):
        super(PurpleairInsertWrapper, self).__init__(conn=conn, query_builder=query_builder, log_filename=log_filename)

    ################################ METHOD FOR INITIALIZE SENSORS AND THEIR INFO ################################
    @log_decorator.log_decorator()
    def initialize_sensors(self, sensor_data: List[Dict[str, Any]], start_id: int):
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
            self.log_info(f"{PurpleairInsertWrapper.__name__}: added sensor '{data[adapt_const.SENS_NAME]}' with id={start_id}")
            start_id += 1

        # Build query to execute
        exec_query = self.builder.initialize_sensors(sensor_values=sensor_values,
                                                     api_param_values=api_param_values,
                                                     location_values=location_values,
                                                     sensor_info_values=sensor_info_values)
        self.conn.send(exec_query)

    ################################ METHOD FOR UPDATE LOCATIONS ################################
    @log_decorator.log_decorator()
    def update_locations(self, changed_sensors: List[Dict[str, Any]], name2id_map: Dict[str, Any]):
        if self.sensor_location_record_builder is None:
            raise SystemExit(f"{PurpleairInsertWrapper.__name__}: bad setup => missing external dependency "
                             f"'{rec.SensorLocationRecord.__name__}'")
        # Build location values to insert
        location_values = []
        for data in changed_sensors:
            sensor_id = name2id_map[data[adapt_const.SENS_NAME]]
            location_values.append(self.sensor_location_record_builder.record(sensor_data=data, sensor_id=sensor_id))
            self.log_info(f"{PurpleairInsertWrapper.__name__}: "
                          f"updated location for sensor '{data[adapt_const.SENS_NAME]}' with sensor_id={sensor_id}")
        # Build query to execute
        exec_query = self.builder.update_locations(location_values)
        # Execute query
        self.conn.send(exec_query)

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

    def __init__(self, conn: db.DatabaseAdapter, query_builder: query.QueryBuilder, log_filename="app"):
        super(AtmotubeInsertWrapper, self).__init__(conn=conn, query_builder=query_builder, log_filename=log_filename)

    @log_decorator.log_decorator()
    def insert_measurements(self, sensor_data: List[Dict[str, Any]], sensor_id: int, channel: str):
        self._exit_on_missing_external_dependencies()

        measure_values = [self.mobile_record_builder.record(sensor_data=data) for data in sensor_data]

        exec_query = self.builder.insert_mobile_measurements(values=measure_values, sensor_id=sensor_id, channel=channel)
        self.conn.send(exec_query)
        self._log_message(sensor_data=sensor_data)

    def _log_message(self, sensor_data: List[Dict[str, Any]]):
        msg_header = f"{AtmotubeInsertWrapper.__name__}:"
        fst_rec_id = sensor_data[0][adapt_const.REC_ID]
        lst_rec_id = sensor_data[-1][adapt_const.REC_ID]
        tot = (lst_rec_id - fst_rec_id) + 1
        self.log_info(f"{msg_header} inserted {tot} mobile records within record_id [{fst_rec_id} - {lst_rec_id}]")

    def _exit_on_missing_external_dependencies(self):
        msg = f"{AtmotubeInsertWrapper.__name__}: bad setup => "

        if self.mobile_record_builder is None:
            raise SystemExit(f"{msg} missing external dependencies 'mobile_record_builder'")


################################ THINGSPEAK INSERT WRAPPER CLASS ################################
class ThingspeakInsertWrapper(InsertWrapper):

    def __init__(self, conn: db.DatabaseAdapter, query_builder: query.QueryBuilder, log_filename="app"):
        super(ThingspeakInsertWrapper, self).__init__(conn=conn, query_builder=query_builder, log_filename=log_filename)

    @log_decorator.log_decorator()
    def insert_measurements(self, sensor_data: List[Dict[str, Any]], sensor_id: int, channel: str):
        self._exit_on_missing_external_dependencies()

        measure_values = [self.station_record_builder.record(sensor_data=data, sensor_id=sensor_id) for data in sensor_data]

        exec_query = self.builder.insert_station_measurements(values=measure_values, sensor_id=sensor_id, channel=channel)
        self.conn.send(exec_query)
        self._log_message(sensor_data=sensor_data)

    def _log_message(self, sensor_data: List[Dict[str, Any]]):
        msg_header = f"{ThingspeakInsertWrapper.__name__}:"
        fst_rec_id = sensor_data[0][adapt_const.REC_ID]
        lst_rec_id = sensor_data[-1][adapt_const.REC_ID]
        tot = (lst_rec_id - fst_rec_id) + 1
        self.log_info(f"{msg_header} inserted {tot} station records within record_id [{fst_rec_id} - {lst_rec_id}]")

    def _exit_on_missing_external_dependencies(self):
        msg = f"{ThingspeakInsertWrapper.__name__}: bad setup =>"

        if self.station_record_builder is None:
            raise SystemExit(f"{msg} missing external dependency 'station_record_builder'")
