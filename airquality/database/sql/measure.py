######################################################
#
# Author: Davide Colombo
# Date: 14/12/21 10:01
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
import itertools
from typing import Dict, List
import airquality.database.sql.abc as sqlabc
import airquality.file.json as filetype
import airquality.api.resp.abc as resptype


# ------------------------------- MeasureSQLBuilderABC ------------------------------- #
class MeasureSQLBuilderABC(sqlabc.SQLBuilderABC, abc.ABC):

    def __init__(self, start_id: int, sensor_id: int, channel_name: str, measure_param: Dict[str, int], sql_queries: filetype.JSONFile):
        self.start_id = start_id
        self.sensor_id = sensor_id
        self.channel_name = channel_name
        self.measure_param = measure_param
        self.sql_file = sql_queries

    @abc.abstractmethod
    def sql(self, data: List[resptype.MeasureAPIRespTypeABC]) -> str:
        pass

    @abc.abstractmethod
    def measure2sql(self, record_id: int, response: resptype.MeasureAPIRespTypeABC) -> str:
        pass


# ------------------------------- MobileMeasureSQLBuilder ------------------------------- #
class MobileMeasureSQLBuilder(MeasureSQLBuilderABC):

    def __init__(self, start_id: int, sensor_id: int, channel_name: str, measure_param: Dict[str, int], sql_queries: filetype.JSONFile):
        super(MobileMeasureSQLBuilder, self).__init__(
            start_id=start_id, sensor_id=sensor_id, channel_name=channel_name, measure_param=measure_param, sql_queries=sql_queries
        )

    ################################ sql() ###############################
    def sql(self, data: List[resptype.MeasureAPIRespTypeABC]) -> str:
        record_id_iter = itertools.count(self.start_id)
        query1 = self.sql_file.i1 + ','.join(self.measure2sql(record_id=next(record_id_iter), response=resp) for resp in data)
        query2 = self.sql_file.u2.format(ts=data[-1].measured_at().ts, sensor_id=self.sensor_id, channel=self.channel_name)
        return f"{query1}; {query2};"

    ################################ measure2sql() ###############################
    def measure2sql(self, record_id: int, response: resptype.MeasureAPIRespTypeABC) -> str:
        ts = response.measured_at().ts
        geom = response.located_at().geom_from_text()
        return ','.join(f"({record_id}, {self.measure_param[m.name]}, '{m.value}', '{ts}', {geom})"
                        if m.value is not None else
                        f"({record_id}, {self.measure_param[m.name]}, NULL, '{ts}', {geom})"
                        for m in response.measures())


# ------------------------------- StationMeasureSQLBuilder ------------------------------- #
class StationMeasureSQLBuilder(MeasureSQLBuilderABC):

    def __init__(self, start_id: int, sensor_id: int, channel_name: str, measure_param: Dict[str, int], sql_queries: filetype.JSONFile):
        super(StationMeasureSQLBuilder, self).__init__(
            start_id=start_id, sensor_id=sensor_id, channel_name=channel_name, measure_param=measure_param, sql_queries=sql_queries
        )

    ################################ sql() ###############################
    def sql(self, data: List[resptype.MeasureAPIRespTypeABC]) -> str:
        record_id_iter = itertools.count(self.start_id)
        query1 = self.sql_file.i2 + ','.join(self.measure2sql(record_id=next(record_id_iter), response=resp) for resp in data)
        query2 = self.sql_file.u2.format(ts=data[-1].measured_at().ts, sensor_id=self.sensor_id, channel=self.channel_name)
        return f"{query1}; {query2};"

    ################################ measure2sql() ###############################
    def measure2sql(self, record_id: int, response: resptype.MeasureAPIRespTypeABC) -> str:
        ts = response.measured_at().ts
        return ','.join(f"({record_id}, {self.measure_param[m.name]}, {self.sensor_id}, '{m.value}', '{ts}')"
                        if m.value is not None else
                        f"({record_id}, {self.measure_param[m.name]}, {self.sensor_id}, NULL, '{ts}')"
                        for m in response.measures())
