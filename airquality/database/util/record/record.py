######################################################
#
# Author: Davide Colombo
# Date: 16/11/21 11:24
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any
import airquality.database.util.record.base as base
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

    def __init__(self, time_rec: t.CurrentTimestampTimeRecord, ts: str = "2018-07-12 11:44:00"):
        self.time_rec = time_rec
        self.valid_from = f"'{ts}'"

    def record(self, sensor_data: Dict[str, Any], sensor_id: int = None) -> str:

        if sensor_id is None:
            raise SystemExit(f"{SensorInfoRecord.__name__}: bad call => missing argument 'sensor_id'")

        self._exit_on_bad_sensor_data(sensor_data)
        geom = sensor_data['geom']['class'](**sensor_data['geom']['kwargs']).geom_from_text()
        return f"({sensor_id}, {self.valid_from}, {geom})"

    def _exit_on_bad_sensor_data(self, sensor_data: Dict[str, Any]):
        _exit_on_missing_geom_data(sensor_data=sensor_data)


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

    def __init__(self, time_rec: t.TimeRecord):
        self.time_rec = time_rec

    def record(self, sensor_data: Dict[str, Any], sensor_id: int = None) -> str:
        self._exit_on_bad_sensor_data(sensor_data)
        record_id = sensor_data['record_id']
        ts = self.time_rec.record(sensor_data)
        geom = sensor_data['geom']['class'](**sensor_data['geom']['kwargs']).geom_from_text()
        records = ','.join(f"({record_id}, {p['id']}, '{p['val']}', {ts}, {geom})" if p['val'] is not None else
                           f"({record_id}, {p['id']}, NULL, {ts}, {geom})" for p in sensor_data['param'])
        return records.strip(',')

    def _exit_on_bad_sensor_data(self, sensor_data: Dict[str, Any]):
        _exit_on_missing_geom_data(sensor_data=sensor_data)
        _exit_on_missing_measure_param_data(sensor_data=sensor_data)


################################ STATION MEASUREMENT RECORD ################################
class StationMeasureRecord(base.RecordBuilder):

    def __init__(self, time_rec: t.TimeRecord):
        self.time_rec = time_rec

    def record(self, sensor_data: Dict[str, Any], sensor_id: int = None) -> str:
        if sensor_id is None:
            raise SystemExit(f"{StationMeasureRecord.__name__}: bad call => missing argument 'sensor_id'")

        self._exit_on_bad_sensor_data(sensor_data)
        record_id = sensor_data['record_id']
        ts = self.time_rec.record(sensor_data)
        records = ','.join(f"({record_id}, {p['id']}, {sensor_id}, '{p['val']}', {ts})" if p['val'] is not None else
                           f"({record_id}, {p['id']}, {sensor_id}, NULL, {ts})" for p in sensor_data['param'])
        return records.strip(',')

    def _exit_on_bad_sensor_data(self, sensor_data: Dict[str, Any]):
        _exit_on_missing_measure_param_data(sensor_data=sensor_data)


########################### FUNCTION FOR CHECKING EXISTENCE OF GEOM ITEM WITHIN SENSOR DATA ############################
def _exit_on_missing_geom_data(sensor_data: Dict[str, Any]):
    if 'geom' not in sensor_data:
        raise SystemExit(f"'{_exit_on_missing_geom_data.__name__}()': bad sensor data => missing key='geom'")
    if not sensor_data['geom']:
        raise SystemExit(f"'{_exit_on_missing_geom_data.__name__}()': bad sensor data => 'geom' cannot be empty")
    if 'class' not in sensor_data['geom'] or 'kwargs' not in sensor_data['geom']:
        raise SystemExit(f"'{_exit_on_missing_geom_data.__name__}()': bad sensor data => 'geom' must have 'class' and "
                         f"'kwargs' keys")


def _exit_on_missing_measure_param_data(sensor_data: Dict[str, Any]):
    if sensor_data.get('record_id') is None:
        raise SystemExit(f"'{_exit_on_missing_measure_param_data.__name__}()': bad sensor data: missing key='record_id'")
    if 'param' not in sensor_data:
        raise SystemExit(f"'{_exit_on_missing_measure_param_data.__name__}()': bad sensor data: missing key='param'")
    if not sensor_data['param']:
        raise SystemExit(f"'{_exit_on_missing_measure_param_data.__name__}()': bad sensor data: empty 'param' list")
    for p in sensor_data['param']:
        if 'id' not in p or 'val' not in p:
            raise SystemExit(f"'{_exit_on_missing_measure_param_data.__name__}()': bad sensor data: missing 'param' keys")
