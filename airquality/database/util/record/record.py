######################################################
#
# Author: Davide Colombo
# Date: 16/11/21 11:24
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any
import airquality.database.util.record.base as base
import airquality.database.util.record.location as loc
import airquality.database.util.record.time as t


################################ SENSOR RECORD ################################
class SensorRecord(base.RecordBuilder):

    def record(self, sensor_data: Dict[str, Any], sensor_id: int = None) -> str:
        self._exit_on_bad_sensor_data(sensor_data)
        sensor_name = sensor_data['name']
        sensor_type = sensor_data['type']
        return f"('{sensor_type}', '{sensor_name}')"

    def _exit_on_bad_sensor_data(self, sensor_data: Dict[str, Any]):
        if sensor_data.get('name') is None:
            raise SystemExit(f"{SensorRecord.__name__}: bad sensor data => missing key='name'")
        if sensor_data.get('type') is None:
            raise SystemExit(f"{SensorRecord.__name__}: bad sensor data => missing key='type'")


################################ API PARAM RECORD ################################
class APIParamRecord(base.RecordBuilder):

    def record(self, sensor_data: Dict[str, Any], sensor_id: int = None) -> str:
        if sensor_id is None:
            raise SystemExit(f"{SensorInfoRecord.__name__}: bad call => missing argument 'sensor_id'")

        self._exit_on_bad_sensor_data(sensor_data)
        values = ','.join(f"({sensor_id}, '{p['param_name']}', '{p['param_value']}')" for p in sensor_data['param'])
        return values.strip(',')

    def _exit_on_bad_sensor_data(self, sensor_data: Dict[str, Any]):
        if 'param' not in sensor_data:
            raise SystemExit(f"{APIParamRecord.__name__}: bad sensor data => missing key='param'")
        if not sensor_data['param']:
            raise SystemExit(f"{APIParamRecord.__name__}: bad sensor data => empty list 'param'")
        for p in sensor_data['param']:
            if 'param_name' not in p or 'param_value' not in p:
                raise SystemExit(f"{APIParamRecord.__name__}: bad sensor data => missing 'param' keys")


################################ SENSOR AT LOCATION RECORD ################################
class SensorLocationRecord(base.RecordBuilder):

    def __init__(self, location_rec: loc.LocationRecord, time_rec: t.CurrentTimestampTimeRecord):
        self.location_rec = location_rec
        self.time_rec = time_rec

    def record(self, sensor_data: Dict[str, Any], sensor_id: int = None) -> str:

        if sensor_id is None:
            raise SystemExit(f"{SensorInfoRecord.__name__}: bad call => missing argument 'sensor_id'")

        self._exit_on_bad_sensor_data(sensor_data)
        valid_from = self.time_rec.record(sensor_data)
        geom = self.location_rec.record(sensor_data)
        return f"({sensor_id}, {valid_from}, {geom})"

    def _exit_on_bad_sensor_data(self, sensor_data: Dict[str, Any]):
        pass


################################ SENSOR INFO RECORD ################################
class SensorInfoRecord(base.RecordBuilder):

    def __init__(self, time_rec: t.TimeRecord):
        self.time_rec = time_rec

    def record(self, sensor_data: Dict[str, Any], sensor_id: int = None) -> str:

        if sensor_id is None:
            raise SystemExit(f"{SensorInfoRecord.__name__}: bad call => missing argument 'sensor_id'")
        self._exit_on_bad_sensor_data(sensor_data)

        records = ','.join(f"({sensor_id}, '{info['channel']}', {self.time_rec.record(info)})"
                           for info in sensor_data['info'])
        return records.strip(',')

    def _exit_on_bad_sensor_data(self, sensor_data: Dict[str, Any]):
        if 'info' not in sensor_data:
            raise SystemExit(f"{SensorInfoRecord.__name__}: bad sensor data => missing key='info'")
        if not sensor_data['info']:
            raise SystemExit(f"{SensorInfoRecord.__name__}: bad sensor data => empty list 'info'")
        for info in sensor_data['info']:
            if 'channel' not in info or 'timestamp' not in info:
                raise SystemExit(f"{SensorInfoRecord.__name__}: bad sensor data => missing 'info' keys")


################################ MOBILE MEASUREMENT RECORD ################################
class MobileMeasureRecord(base.RecordBuilder):

    def __init__(self, time_rec: t.TimeRecord, location_rec: loc.LocationRecord):
        self.time_rec = time_rec
        self.location_rec = location_rec

    def record(self, sensor_data: Dict[str, Any], sensor_id: int = None) -> str:
        self._exit_on_bad_sensor_data(sensor_data)
        record_id = sensor_data['record_id']
        param_id = sensor_data['param_id']
        param_val = sensor_data['param_value']
        ts = self.time_rec.record(sensor_data)
        geom = self.location_rec.record(sensor_data)
        records = ','.join(f"({record_id}, {id_}, '{value}', {ts}, {geom})" if value is not None else
                           f"({record_id}, {id_}, NULL, {ts}, {geom})" for id_, value in zip(param_id, param_val))
        return records.strip(',')

    def _exit_on_bad_sensor_data(self, sensor_data: Dict[str, Any]):

        if sensor_data.get('record_id') is None:
            raise SystemExit(f"{MobileMeasureRecord.__name__}: bad sensor data: missing key='record_id'")
        if sensor_data.get('param_id') is None:
            raise SystemExit(f"{MobileMeasureRecord.__name__}: bad sensor data: missing key='param_id'")
        if sensor_data.get('param_value') is None:
            raise SystemExit(f"{MobileMeasureRecord.__name__}: bad sensor data: missing key='param_value'")

        if not sensor_data['param_value'] or not sensor_data['param_id']:
            raise SystemExit(f"{MobileMeasureRecord.__name__}: bad packet => please check you packet has a non-empty list"
                             f"of param id(s) and a non-empty list of param value(s), one for each name(s).")

        if len(sensor_data['param_value']) != len(sensor_data['param_id']):
            raise SystemExit(f"{MobileMeasureRecord.__name__}: bad packet => number of param id(s) does not match the "
                             f"number of param value(s)")


################################ STATION MEASUREMENT RECORD ################################
class StationMeasureRecord(base.RecordBuilder):

    def __init__(self, time_rec: t.TimeRecord):
        self.time_rec = time_rec

    def record(self, sensor_data: Dict[str, Any], sensor_id: int = None) -> str:

        if sensor_id is None:
            raise SystemExit(f"{StationMeasureRecord.__name__}: bad call => missing argument 'sensor_id'")

        self._exit_on_bad_sensor_data(sensor_data)
        record_id = sensor_data['record_id']
        param_id = sensor_data['param_id']
        param_val = sensor_data['param_value']
        ts = self.time_rec.record(sensor_data)
        records = ','.join(f"({record_id}, {id_}, {sensor_id}, '{val}', {ts})" for id_, val in zip(param_id, param_val))
        return records.strip(',')

    def _exit_on_bad_sensor_data(self, sensor_data: Dict[str, Any]):

        if sensor_data.get('record_id') is None:
            raise SystemExit(f"{StationMeasureRecord.__name__}: bad sensor data: missing key='record_id'")
        if sensor_data.get('param_id') is None:
            raise SystemExit(f"{StationMeasureRecord.__name__}: bad sensor data: missing key='param_id'")
        if sensor_data.get('param_value') is None:
            raise SystemExit(f"{StationMeasureRecord.__name__}: bad sensor data: missing key='param_value'")

        if not sensor_data['param_value'] or not sensor_data['param_id']:
            raise SystemExit(f"{StationMeasureRecord.__name__}: bad packet => please check you packet has a non-empty list"
                             f"of param id(s) and a non-empty list of param value(s), one for each name(s).")

        if len(sensor_data['param_value']) != len(sensor_data['param_id']):
            raise SystemExit(f"{StationMeasureRecord.__name__}: bad packet => number of param id(s) does not match the "
                             f"number of param value(s)")
