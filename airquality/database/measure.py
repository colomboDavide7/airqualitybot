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
import airquality.database.abc as sqlabc
import airquality.file.json as filetype
import airquality.api.resp.abc as resptype
import airquality.database.adapt as dbtype


# ------------------------------- MeasureSQLBuilderABC ------------------------------- #
class MeasureDBRepoABC(sqlabc.DBRepoABC, abc.ABC):

    def __init__(self, sensor_id: int, channel_name: str, measure_param: Dict[str, int], db_adapter: dbtype.DBAdaptABC, sql_queries: filetype.JSONFile):
        self.sensor_id = sensor_id
        self.channel_name = channel_name
        self.measure_param = measure_param
        self.db_adapter = db_adapter
        self.sql_queries = sql_queries

    @abc.abstractmethod
    def push(self, data: List[resptype.MeasureAPIRespTypeABC]) -> str:
        pass

    @abc.abstractmethod
    def measure2sql(self, record_id: int, response: resptype.MeasureAPIRespTypeABC) -> str:
        pass


# ------------------------------- MobileMeasureSQLBuilder ------------------------------- #
class MobileMeasureDBRepo(MeasureDBRepoABC):

    @property
    def max_mobile_record_id(self) -> int:
        query2exec = self.sql_queries.s9
        db_lookup = self.db_adapter.execute(query2exec)
        max_record_id = db_lookup[0][0]
        return 1 if max_record_id is None else (max_record_id + 1)

    ################################ push() ###############################
    def push(self, data: List[resptype.MeasureAPIRespTypeABC]) -> None:
        record_id_iter = itertools.count(self.max_mobile_record_id)
        query1 = self.sql_queries.i1 + ','.join(self.measure2sql(record_id=next(record_id_iter), response=resp) for resp in data)
        query2 = self.sql_queries.u2.format(ts=data[-1].measured_at().ts, sensor_id=self.sensor_id, channel=self.channel_name)
        query2exec = f"{query1}; {query2};"
        self.db_adapter.execute(query2exec)

    ################################ measure2sql() ###############################
    def measure2sql(self, record_id: int, response: resptype.MeasureAPIRespTypeABC) -> str:
        ts = response.measured_at().ts
        geom = response.located_at().geom_from_text()
        return ','.join(f"({record_id}, {self.measure_param[m.name]}, '{m.value}', '{ts}', {geom})"
                        if m.value is not None else
                        f"({record_id}, {self.measure_param[m.name]}, NULL, '{ts}', {geom})"
                        for m in response.measures())


# ------------------------------- StationMeasureSQLBuilder ------------------------------- #
class StationMeasureDBRepo(MeasureDBRepoABC):

    @property
    def max_station_record_id(self) -> int:
        query2exec = self.sql_queries.s10
        db_lookup = self.db_adapter.execute(query2exec)
        max_record_id = db_lookup[0][0]
        return 1 if max_record_id is None else (max_record_id + 1)

    ################################ push() ###############################
    def push(self, data: List[resptype.MeasureAPIRespTypeABC]) -> None:
        record_id_iter = itertools.count(self.max_station_record_id)
        query1 = self.sql_queries.i2 + ','.join(self.measure2sql(record_id=next(record_id_iter), response=resp) for resp in data)
        query2 = self.sql_queries.u2.format(ts=data[-1].measured_at().ts, sensor_id=self.sensor_id, channel=self.channel_name)
        query2exec = f"{query1}; {query2};"
        self.db_adapter.execute(query2exec)

    ################################ measure2sql() ###############################
    def measure2sql(self, record_id: int, response: resptype.MeasureAPIRespTypeABC) -> str:
        ts = response.measured_at().ts
        return ','.join(f"({record_id}, {self.measure_param[m.name]}, {self.sensor_id}, '{m.value}', '{ts}')"
                        if m.value is not None else
                        f"({record_id}, {self.measure_param[m.name]}, {self.sensor_id}, NULL, '{ts}')"
                        for m in response.measures())
