######################################################
#
# Author: Davide Colombo
# Date: 12/12/21 09:32
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import itertools
from typing import List
import airquality.database.exe.abc as recabc
import airquality.api.resp.abc as resptype
import airquality.types.timestamp as tstype
import airquality.database.repo.info as dbrepo


class InfoQueryExecutor(recabc.QueryExecutorABC):

    def __init__(self, db_repo: dbrepo.SensorInfoRepo):
        self._db_repo = db_repo

    ################################ build() ###############################
    def execute(self, data: List[resptype.InfoAPIRespTypeABC]) -> None:
        sensor_values = self._db_repo.sensor_query
        apiparam_values = self._db_repo.apiparam_query
        geolocation_values = self._db_repo.geolocation_query

        start_index = self._db_repo.max_sensor_id
        sensor_id_iter = itertools.count(start_index)
        for d in data:
            sensor_id = next(sensor_id_iter)
            sensor_values += self._sensor2sql(sensor_id=sensor_id, response=d)
            apiparam_values += self._apiparam2sql(sensor_id=sensor_id, response=d)
            geolocation_values += self._geo2sql(sensor_id=sensor_id, response=d)

        query2exec = f"{sensor_values.strip(',')}; {apiparam_values.strip(',')}; {geolocation_values.strip(',')};"
        self._db_repo.push(query2exec)

    ################################ _sensor2sql() ###############################
    def _sensor2sql(self, sensor_id: int, response: resptype.InfoAPIRespTypeABC) -> str:
        return f"({sensor_id}, '{response.sensor_type()}', '{response.sensor_name()}'),"

    ################################ _apiparam2sql() ###############################
    def _apiparam2sql(self, sensor_id: int, response: resptype.InfoAPIRespTypeABC) -> str:
        timestamp = response.date_created().ts
        return ','.join(f"({sensor_id}, '{c.key}', '{c.ident}', '{c.name}', '{timestamp}')" for c in response.channels()) + ','

    ################################ _geo2sql() ###############################
    def _geo2sql(self, sensor_id: int, response: resptype.InfoAPIRespTypeABC) -> str:
        timestamp = tstype.CurrentTimestamp().ts
        geom = response.geolocation().geom_from_text()
        return f"({sensor_id}, '{timestamp}', {geom}),"
