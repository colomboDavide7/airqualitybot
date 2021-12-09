######################################################
#
# Author: Davide Colombo
# Date: 26/11/21 10:43
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List, Dict
import airquality.types.timestamp as ts
import airquality.types.postgis as pgis


# class MeasureAPIResp:
#
#     def __init__(self, timestamp: ts.Timestamp, measures: List[ParamNameValue]):
#         self.timestamp = timestamp
#         self.measures = measures
#
#     def measure2sql(self, record_id: int, sensor_id: int, code2id: Dict[str, int]) -> str:
#         fmt_ts = self.timestamp.ts
#         return ','.join(f"({record_id}, {code2id[m.name]}, {sensor_id}, '{m.value}', '{fmt_ts}')" if m.value is not None else
#                         f"({record_id}, {code2id[m.name]}, {sensor_id}, NULL, '{fmt_ts}')" for m in self.measures) + ','
#
#
# ################################ MOBILE SENSOR API RESPONSE ################################
# class MobileSensorAPIResp(MeasureAPIResp):
#
#     def __init__(self, timestamp: ts.Timestamp, measures: List[ParamNameValue], geometry: pgis.PostgisPoint):
#         super(MobileSensorAPIResp, self).__init__(timestamp=timestamp, measures=measures)
#         self.geometry = geometry
#
#     def measure2sql(self, record_id: int, code2id: Dict[str, int], sensor_id=None) -> str:
#         fmt_ts = self.timestamp.ts
#         geom = self.geometry.geom_from_text()
#         return ','.join(f"({record_id}, {code2id[m.name]}, '{m.value}', '{fmt_ts}', {geom})" if m.value is not None else
#                         f"({record_id}, {code2id[m.name]}, NULL, '{fmt_ts}', {geom})" for m in self.measures) + ','
