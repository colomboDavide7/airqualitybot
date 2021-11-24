######################################################
#
# Author: Davide Colombo
# Date: 16/11/21 11:24
# Description: INSERT HERE THE DESCRIPTION
#
######################################################

# ################################ MOBILE MEASUREMENT RECORD ################################
# class MobileMeasureRecord(base.RecordBuilder):
#
#     def __init__(self, time_rec: t.TimeRecord, location_rec: loc.LocationRecord):
#         self.time_rec = time_rec
#         self.location_rec = location_rec
#
#     def rec(self, sensor_data: Dict[str, Any], sensor_id: int = None) -> str:
#         self._exit_on_bad_sensor_data(sensor_data)
#         record_id = sensor_data[c.REC_ID]
#         ts = self.time_rec.rec(sensor_data=sensor_data)
#         geom = self.location_rec.rec(sensor_data=sensor_data)
#         records = ','.join(f"({record_id}, {p[c.PAR_ID]}, '{p[c.PAR_VAL]}', {ts}, {geom})" if p[c.PAR_VAL] is not None else
#                            f"({record_id}, {p[c.PAR_ID]}, NULL, {ts}, {geom})" for p in sensor_data[c.SENS_PARAM])
#         return records.strip(',')
#
#     def _exit_on_bad_sensor_data(self, sensor_data: Dict[str, Any]):
#         _exit_on_missing_measure_param_data(sensor_data=sensor_data)
#
#
# ################################ STATION MEASUREMENT RECORD ################################
# class StationMeasureRecord(base.RecordBuilder):
#
#     def __init__(self, time_rec: t.TimeRecord):
#         self.time_rec = time_rec
#
#     def rec(self, sensor_data: Dict[str, Any], sensor_id: int = None) -> str:
#         self._exit_on_bad_sensor_data(sensor_data)
#         if sensor_id is None:
#             raise SystemExit(f"{StationMeasureRecord.__name__}: bad call => missing argument 'sensor_id'")
#
#         record_id = sensor_data[c.REC_ID]
#         ts = self.time_rec.rec(sensor_data=sensor_data)
#         records = ','.join(f"({record_id}, {p[c.PAR_ID]}, {sensor_id}, '{p[c.PAR_VAL]}', {ts})" if p[c.PAR_VAL] is not None else
#                            f"({record_id}, {p[c.PAR_ID]}, {sensor_id}, NULL, {ts})" for p in sensor_data[c.SENS_PARAM])
#         return records.strip(',')
#
#     def _exit_on_bad_sensor_data(self, sensor_data: Dict[str, Any]):
#         _exit_on_missing_measure_param_data(sensor_data=sensor_data)
