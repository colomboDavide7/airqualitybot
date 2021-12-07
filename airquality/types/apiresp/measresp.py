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


class ParamNameValue:

    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value


class MeasureAPIResp:

    def __init__(self, timestamp: ts.Timestamp, measures: List[ParamNameValue]):
        self.timestamp = timestamp
        self.measures = measures


################################ MOBILE SENSOR API RESPONSE ################################
class MobileSensorAPIResp(MeasureAPIResp):

    def __init__(self, timestamp: ts.Timestamp, measures: List[ParamNameValue], geometry: pgis.PostgisPoint):
        super(MobileSensorAPIResp, self).__init__(timestamp=timestamp, measures=measures)
        self.geometry = geometry

    def measure2sql(self, record_id: int, code2id: Dict[str, int]) -> str:
        fmt_ts = self.timestamp.get_formatted_timestamp()
        geom = self.geometry.geom_from_text()
        return ','.join(f"({record_id}, {code2id[m.name]}, '{m.value}', '{fmt_ts}', {geom})" if m.value is not None else
                        f"({record_id}, {code2id[m.name]}, NULL, '{fmt_ts}', {geom})" for m in self.measures) + ','
