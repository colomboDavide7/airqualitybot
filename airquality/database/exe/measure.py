######################################################
#
# Author: Davide Colombo
# Date: 12/12/21 12:30
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
import itertools
from typing import List
import airquality.database.exe.abc as recabc
import airquality.database.repo.measure as dbrepo
import airquality.api.resp.abc as resptype


# ------------------------------- MeasureQueryExecutorABC ------------------------------- #
class MeasureQueryExecutorABC(recabc.QueryExecutorABC, abc.ABC):

    def __init__(self, sensor_id: int, channel_name: str, db_repo: dbrepo.SensorMeasureRepo):
        self._sensor_id = sensor_id
        self._channel_name = channel_name
        self._db_repo = db_repo

    @abc.abstractmethod
    def measure2sql(self, record_id: int, response: resptype.MeasureAPIRespTypeABC) -> str:
        pass


# ------------------------------- MobileMeasureQueryExecutor ------------------------------- #
class MobileMeasureQueryExecutor(MeasureQueryExecutorABC):

    def __init__(self, sensor_id: int, channel_name: str, db_repo: dbrepo.SensorMeasureRepo):
        super(MobileMeasureQueryExecutor, self).__init__(sensor_id=sensor_id, channel_name=channel_name, db_repo=db_repo)

    ################################ execute() ###############################
    def execute(self, data: List[resptype.MeasureAPIRespTypeABC]) -> None:
        start_index = self._db_repo.max_mobile_record_id
        record_id_iter = itertools.count(start_index)
        query1 = self._db_repo.mobile_measure_query
        query1 += ','.join(self.measure2sql(record_id=next(record_id_iter), response=resp) for resp in data)
        query2 = self._db_repo.update_channel_acquisition_query.format(
            ts=data[-1].measured_at().ts, sensor_id=self._sensor_id, channel=self._channel_name
        )
        query2exec = f"{query1}; {query2};"
        self._db_repo.push(query2exec)

    ################################ measure2sql() ###############################
    def measure2sql(self, record_id: int, response: resptype.MeasureAPIRespTypeABC):
        ts = response.measured_at().ts
        geom = response.located_at().geom_from_text()
        code2id = self._db_repo.measure_param
        return ','.join(f"({record_id}, {code2id[m.name]}, '{m.value}', '{ts}', {geom})"
                        if m.value is not None else
                        f"({record_id}, {code2id[m.name]}, NULL, '{ts}', {geom})"
                        for m in response.measures())
