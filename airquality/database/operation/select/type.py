######################################################
#
# Author: Davide Colombo
# Date: 17/11/21 16:44
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import List, Dict, Any
import airquality.database.operation.base as base
import airquality.database.util.conn as db
import airquality.database.util.query as query


def get_type_select_wrapper(sensor_type: str, conn: db.DatabaseAdapter, query_builder: query.QueryBuilder):

    if sensor_type in ('purpleair', 'thingspeak'):
        return StationTypeSelectWrapper(conn=conn, query_builder=query_builder, sensor_type=sensor_type)
    elif sensor_type == 'atmotube':
        return MobileTypeSelectWrapper(conn=conn, query_builder=query_builder, sensor_type=sensor_type)
    else:
        raise SystemExit(f"'{get_type_select_wrapper.__name__}():' bad type '{sensor_type}'")


################################ TYPE SELECT WRAPPER BASE CLASS ################################
class TypeSelectWrapper(base.DatabaseOperationWrapper, abc.ABC):

    def __init__(self, conn: db.DatabaseAdapter, query_builder: query.QueryBuilder, sensor_type: str):
        super(TypeSelectWrapper, self).__init__(conn=conn, query_builder=query_builder)
        self.sensor_type = sensor_type

    def get_sensor_id(self) -> List[int]:
        exec_query = self.builder.select_sensor_ids_from_sensor_type(self.sensor_type)
        answer = self.conn.send(exec_query)
        return [t[0] for t in answer]

    def get_measure_param(self) -> Dict[str, Any]:
        exec_query = self.builder.select_measure_param_from_sensor_type(self.sensor_type)
        answer = self.conn.send(exec_query)
        return dict(answer)

    def get_sensor_names(self) -> List[str]:
        exec_query = self.builder.select_sensor_names_from_sensor_type(self.sensor_type)
        answer = self.conn.send(exec_query)
        return [t[0] for t in answer]

    def get_name_id_map(self) -> Dict[str, Any]:
        exec_query = self.builder.select_sensor_name_id_mapping_from_sensor_type(self.sensor_type)
        answer = self.conn.send(exec_query)
        return dict(answer)

    def get_max_sensor_id(self) -> int:
        exec_query = self.builder.select_max_sensor_id()
        answer = self.conn.send(exec_query)
        unfolded = [t[0] for t in answer]
        return 1 if unfolded[0] is None else (unfolded[0] + 1)

    def get_active_locations(self) -> Dict[str, Any]:
        exec_query = self.builder.select_active_locations(sensor_type=self.sensor_type)
        answer = self.conn.send(exec_query)
        return dict(answer)

    @abc.abstractmethod
    def get_max_record_id(self) -> int:
        pass


################################ MOBILE TYPE SELECT WRAPPER ################################
class MobileTypeSelectWrapper(TypeSelectWrapper):

    def __init__(self, conn: db.DatabaseAdapter, query_builder: query.QueryBuilder, sensor_type: str):
        super(MobileTypeSelectWrapper, self).__init__(conn=conn, query_builder=query_builder, sensor_type=sensor_type)

    def get_max_record_id(self) -> int:
        exec_query = self.builder.select_max_mobile_record_id()
        answer = self.conn.send(exec_query)
        unfolded = [t[0] for t in answer]
        return 1 if unfolded[0] is None else (unfolded[0] + 1)


################################ STATION TYPE SELECT WRAPPER ################################
class StationTypeSelectWrapper(TypeSelectWrapper):

    def __init__(self, conn: db.DatabaseAdapter, query_builder: query.QueryBuilder, sensor_type: str):
        super(StationTypeSelectWrapper, self).__init__(conn=conn, query_builder=query_builder, sensor_type=sensor_type)

    def get_active_locations(self) -> Dict[str, Any]:
        exec_query = self.builder.select_active_locations(self.sensor_type)
        answer = self.conn.send(exec_query)
        return dict(answer)

    def get_max_record_id(self) -> int:
        exec_query = self.builder.select_max_station_record_id()
        answer = self.conn.send(exec_query)
        unfolded = [t[0] for t in answer]
        return 1 if unfolded[0] is None else (unfolded[0] + 1)


################################ SENSOR ID SELECT WRAPPER ################################
class SensorIDSelectWrapper(base.DatabaseOperationWrapper):

    def __init__(self, conn: db.DatabaseAdapter, query_builder: query.QueryBuilder):
        super(SensorIDSelectWrapper, self).__init__(conn=conn, query_builder=query_builder)

    def get_sensor_api_param(self, sensor_id: int) -> Dict[str, Any]:
        self.log_info(f"{SensorIDSelectWrapper.__name__}: try to query API param for sensor_id='{sensor_id}...")
        exec_query = self.builder.select_api_param_from_sensor_id(sensor_id)
        answer = self.conn.send(exec_query)
        self.log_info(f"{SensorIDSelectWrapper.__name__}: done")
        return dict(answer)

    def get_last_acquisition(self, channel: str, sensor_id: int) -> str:
        self.log_info(f"{SensorIDSelectWrapper.__name__}: try to query last acquisition for sensor_id='{sensor_id} on "
                      f"channel='{channel}'...")
        exec_query = self.builder.select_last_acquisition(channel=channel, sensor_id=sensor_id)
        answer = self.conn.send(exec_query)
        unfolded = [str(t[0]) for t in answer]

        if not unfolded:
            raise SystemExit(f"{SensorIDSelectWrapper.__name__}: bad database answer => cannot retrieve last acquisition "
                             f"timestamp for sensor_id={sensor_id} and channel='{channel}'")

        self.log_info(f"{SensorIDSelectWrapper.__name__}: done")
        return unfolded[0]
