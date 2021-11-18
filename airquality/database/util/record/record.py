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
import airquality.database.util.record.location as loc
import airquality.adapter.config as c


################################ SENSOR RECORD ################################
class SensorRecord(base.RecordBuilder):

    def record(self, sensor_data: Dict[str, Any], sensor_id: int = None) -> str:
        self._exit_on_bad_sensor_data(sensor_data)
        sensor_name = sensor_data[c.SENS_NAME]
        sensor_type = sensor_data[c.SENS_TYPE]
        return f"('{sensor_type}', '{sensor_name}')"

    def _exit_on_bad_sensor_data(self, sensor_data: Dict[str, Any]):
        msg = f"{SensorRecord.__name__}: bad sensor data =>"

        if sensor_data.get(c.SENS_NAME) is None:
            raise SystemExit(f"{msg} missing key='{c.SENS_NAME}'")
        if sensor_data.get(c.SENS_TYPE) is None:
            raise SystemExit(f"{msg} missing key='{c.SENS_TYPE}'")


################################ API PARAM RECORD ################################
class APIParamRecord(base.RecordBuilder):

    def record(self, sensor_data: Dict[str, Any], sensor_id: int = None) -> str:
        if sensor_id is None:
            raise SystemExit(f"{SensorInfoRecord.__name__}: bad call => missing argument 'sensor_id'")

        self._exit_on_bad_sensor_data(sensor_data)
        values = ','.join(f"({sensor_id}, '{p[c.PAR_NAME]}', '{p[c.PAR_VAL]}')" for p in sensor_data[c.SENS_PARAM])
        return values.strip(',')

    def _exit_on_bad_sensor_data(self, sensor_data: Dict[str, Any]):
        msg = f"{APIParamRecord.__name__}: bad sensor data =>"

        if c.SENS_PARAM not in sensor_data:
            raise SystemExit(f"{msg} missing key='{c.SENS_PARAM}'")
        if not sensor_data[c.SENS_PARAM]:
            raise SystemExit(f"{msg} empty list '{c.SENS_PARAM}'")
        for p in sensor_data[c.SENS_PARAM]:
            if c.PAR_NAME not in p or c.PAR_VAL not in p:
                raise SystemExit(f"{msg} missing '{c.SENS_PARAM}' keys '{c.PAR_NAME}', '{c.PAR_VAL}'")


################################ SENSOR AT LOCATION RECORD ################################
class SensorLocationRecord(base.RecordBuilder):

    def __init__(self, time_rec: t.TimeRecord, location_rec: loc.LocationRecord):
        self.time_rec = time_rec
        self.location_rec = location_rec

    def record(self, sensor_data: Dict[str, Any], sensor_id: int = None) -> str:
        self._exit_on_bad_sensor_data(sensor_data)
        if sensor_id is None:
            raise SystemExit(f"{SensorInfoRecord.__name__}: bad call => missing argument 'sensor_id'")

        valid_from = self.time_rec.record(sensor_data=sensor_data)
        geom = self.location_rec.record(sensor_data=sensor_data)
        return f"({sensor_id}, {valid_from}, {geom})"

    def _exit_on_bad_sensor_data(self, sensor_data: Dict[str, Any]):
        pass


################################ SENSOR INFO RECORD ################################
class SensorInfoRecord(base.RecordBuilder):

    def __init__(self, time_rec: t.TimeRecord):
        self.time_rec = time_rec

    def record(self, sensor_data: Dict[str, Any], sensor_id: int = None) -> str:
        self._exit_on_bad_sensor_data(sensor_data)
        if sensor_id is None:
            raise SystemExit(f"{SensorInfoRecord.__name__}: bad call => missing argument 'sensor_id'")

        records = ','.join(f"({sensor_id}, '{info[c.SENS_CH]}', {self.time_rec.record(info)})" for info in sensor_data[c.SENS_INFO])
        return records.strip(',')

    def _exit_on_bad_sensor_data(self, sensor_data: Dict[str, Any]):
        msg = f"{SensorInfoRecord.__name__}: bad sensor data =>"

        if c.SENS_INFO not in sensor_data:
            raise SystemExit(f"{msg} missing key='{c.SENS_INFO}'")
        if not sensor_data[c.SENS_INFO]:
            raise SystemExit(f"{msg} empty list '{c.SENS_INFO}'")
        for info in sensor_data[c.SENS_INFO]:
            if c.SENS_CH not in info or c.TIMEST not in info:
                raise SystemExit(f"{msg} missing '{c.SENS_INFO}' keys '{c.SENS_CH}', '{c.TIMEST}'")


################################ MOBILE MEASUREMENT RECORD ################################
class MobileMeasureRecord(base.RecordBuilder):

    def __init__(self, time_rec: t.TimeRecord, location_rec: loc.LocationRecord):
        self.time_rec = time_rec
        self.location_rec = location_rec

    def record(self, sensor_data: Dict[str, Any], sensor_id: int = None) -> str:
        self._exit_on_bad_sensor_data(sensor_data)
        record_id = sensor_data[c.REC_ID]
        ts = self.time_rec.record(sensor_data=sensor_data)
        geom = self.location_rec.record(sensor_data=sensor_data)
        records = ','.join(f"({record_id}, {p[c.PAR_ID]}, '{p[c.PAR_VAL]}', {ts}, {geom})" if p[c.PAR_VAL] is not None else
                           f"({record_id}, {p[c.PAR_ID]}, NULL, {ts}, {geom})" for p in sensor_data[c.SENS_PARAM])
        return records.strip(',')

    def _exit_on_bad_sensor_data(self, sensor_data: Dict[str, Any]):
        _exit_on_missing_measure_param_data(sensor_data=sensor_data)


################################ STATION MEASUREMENT RECORD ################################
class StationMeasureRecord(base.RecordBuilder):

    def __init__(self, time_rec: t.TimeRecord):
        self.time_rec = time_rec

    def record(self, sensor_data: Dict[str, Any], sensor_id: int = None) -> str:
        self._exit_on_bad_sensor_data(sensor_data)
        if sensor_id is None:
            raise SystemExit(f"{StationMeasureRecord.__name__}: bad call => missing argument 'sensor_id'")

        record_id = sensor_data[c.REC_ID]
        ts = self.time_rec.record(sensor_data=sensor_data)
        records = ','.join(f"({record_id}, {p[c.PAR_ID]}, {sensor_id}, '{p[c.PAR_VAL]}', {ts})" if p[c.PAR_VAL] is not None else
                           f"({record_id}, {p[c.PAR_ID]}, {sensor_id}, NULL, {ts})" for p in sensor_data[c.SENS_PARAM])
        return records.strip(',')

    def _exit_on_bad_sensor_data(self, sensor_data: Dict[str, Any]):
        _exit_on_missing_measure_param_data(sensor_data=sensor_data)


########################### FUNCTION FOR CHECKING EXISTENCE OF GEOM ITEM WITHIN SENSOR DATA ############################
def _exit_on_missing_measure_param_data(sensor_data: Dict[str, Any]):
    msg = f"'{_exit_on_missing_measure_param_data.__name__}()': bad sensor data =>"

    if sensor_data.get(c.REC_ID) is None:
        raise SystemExit(f"{msg} missing key='{c.REC_ID}'")
    if c.SENS_PARAM not in sensor_data:
        raise SystemExit(f"{msg} missing key='{c.SENS_PARAM}'")
    if not sensor_data[c.SENS_PARAM]:
        raise SystemExit(f"{msg} empty '{c.SENS_PARAM}' list")
    for p in sensor_data[c.SENS_PARAM]:
        if c.PAR_ID not in p or c.PAR_VAL not in p:
            raise SystemExit(f"{msg} missing '{c.SENS_PARAM}' keys '{c.PAR_ID}', '{c.PAR_VAL}'")
