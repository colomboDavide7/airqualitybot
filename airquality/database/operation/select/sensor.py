######################################################
#
# Author: Davide Colombo
# Date: 17/11/21 16:44
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import List, Dict, Any
import airquality.database.operation.baseoprt as base
import airquality.database.util.conn as db
import airquality.database.util.query as query
import airquality.logger.util.decorator as log_decorator


################################ SENSOR DATA SELECTOR BASE CLASS ################################
class SensorDataSelector(base.DatabaseOperationWrapper, abc.ABC):

    def __init__(self, conn: db.DatabaseAdapter, query_builder: query.QueryBuilder, sensor_type: str):
        super(SensorDataSelector, self).__init__(conn=conn, query_builder=query_builder)
        self.sensor_type = sensor_type

    @abc.abstractmethod
    def select(self) -> List[Dict[str, Any]]:
        pass

    def _select_api_param(self, data: Dict[str, Any], sensor_id: int) -> Dict[str, Any]:
        exec_query = self.builder.select_api_param_from_sensor_id(sensor_id=sensor_id)
        api_param = self.conn.send(exec_query)
        for param_name, param_value in api_param:
            data[param_name] = param_value
        return data

    def _select_channel_info(self, data: Dict[str, Any], sensor_id: int) -> Dict[str, Any]:
        exec_query = self.builder.select_channel_info_from_sensor_id(sensor_id=sensor_id)
        info = self.conn.send(exec_query)
        for channel_name, last_acquisition in info:
            data[channel_name] = last_acquisition
        return data


################################ STATION SENSOR DATA SELECTOR ################################
class StationSensorDataSelector(SensorDataSelector):

    def __init__(self, conn: db.DatabaseAdapter, query_builder: query.QueryBuilder, sensor_type: str):
        super(StationSensorDataSelector, self).__init__(conn=conn, query_builder=query_builder, sensor_type=sensor_type)

    @log_decorator.log_decorator()
    def select(self) -> List[Dict[str, Any]]:
        sensor_data = []
        exec_query = self.builder.select_sensor_id_name_type_from_type(self.sensor_type)
        sensors = self.conn.send(exec_query)
        for sensor_id, sensor_name, sensor_type in sensors:
            data = {"sensor_id": sensor_id, "sensor_name": sensor_name, "sensor_type": sensor_type}
            data = self._select_api_param(data=data, sensor_id=sensor_id)
            data = self._select_channel_info(data=data, sensor_id=sensor_id)
            data = self._select_sensor_location(data=data, sensor_id=sensor_id)
            sensor_data.append(data)
        self.log_info(f"{StationSensorDataSelector.__name__}: found {len(sensor_data)} database sensors")
        return sensor_data

    def _select_sensor_location(self, data: Dict[str, Any], sensor_id: int) -> Dict[str, Any]:
        exec_query = self.builder.select_location_from_sensor_id(sensor_id=sensor_id)
        active_locations = self.conn.send(exec_query)
        for longitude, latitude in active_locations:
            data["longitude"] = longitude
            data["latitude"] = latitude
        return data


################################ MOBILE SENSOR DATA SELECTOR ################################
class MobileSensorDataSelector(SensorDataSelector):

    def __init__(self, conn: db.DatabaseAdapter, query_builder: query.QueryBuilder, sensor_type: str):
        super(MobileSensorDataSelector, self).__init__(conn=conn, query_builder=query_builder, sensor_type=sensor_type)

    def select(self) -> List[Dict[str, Any]]:
        sensor_data = []
        exec_query = self.builder.select_sensor_id_name_type_from_type(sensor_type=self.sensor_type)
        sensors = self.conn.send(exec_query)
        for sensor_id, sensor_name, sensor_type in sensors:
            data = {"sensor_id": sensor_id, "sensor_name": sensor_name, "sensor_type": sensor_type}
            data = self._select_api_param(data=data, sensor_id=sensor_id)
            data = self._select_channel_info(data=data, sensor_id=sensor_id)
            sensor_data.append(data)
        self.log_info(f"{MobileSensorDataSelector.__name__}: found {len(sensor_data)} database sensors")
        return sensor_data
