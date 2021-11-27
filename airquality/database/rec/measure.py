######################################################
#
# Author: Davide Colombo
# Date: 26/11/21 12:19
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import Dict, Any
import airquality.types.apiresp.measresp as resp


class MeasureRecord(abc.ABC):

    def __init__(self, record_id: int, sensor_id: int, name2id: Dict[str, Any], response: resp.MeasureAPIResp):
        self.record_id = record_id
        self.name2id = name2id
        self.sensor_id = sensor_id
        self.response = response

    @abc.abstractmethod
    def get_measure_values(self) -> str:
        pass


################################ MOBILE MEASURE RECORD ################################
class MobileMeasureRecord(MeasureRecord):

    def __init__(self, record_id: int, sensor_id: int, response: resp.MobileSensorAPIResp, name2id: Dict[str, Any]):
        super(MobileMeasureRecord, self).__init__(record_id=record_id, sensor_id=sensor_id, name2id=name2id, response=response)
        self.response = response

    def get_measure_values(self) -> str:
        fmt_ts = self.response.timestamp.get_formatted_timestamp()
        geom = self.response.geometry.geom_from_text()
        return ','.join(f"({self.record_id}, {self.name2id[m.name]}, '{m.value}', '{fmt_ts}', {geom})"
                        if m.value is not None else
                        f"({self.record_id}, {self.name2id[m.name]}, NULL, '{fmt_ts}', {geom})"
                        for m in self.response.measures)


################################ STATION MEASURE RECORD ################################
class StationMeasureRecord(MeasureRecord):

    def __init__(self, record_id: int, sensor_id: int, response: resp.MeasureAPIResp, name2id: Dict[str, Any]):
        super(StationMeasureRecord, self).__init__(record_id=record_id, sensor_id=sensor_id, name2id=name2id, response=response)
        self.response = response

    def get_measure_values(self) -> str:
        fmt_ts = self.response.timestamp.get_formatted_timestamp()
        return ','.join(f"({self.record_id}, {self.name2id[m.name]}, {self.sensor_id}, '{m.value}', '{fmt_ts}')"
                        if m.value is not None else
                        f"({self.record_id}, {self.name2id[m.name]}, {self.sensor_id}, NULL, '{fmt_ts}')"
                        for m in self.response.measures)
