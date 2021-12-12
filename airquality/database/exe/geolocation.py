######################################################
#
# Author: Davide Colombo
# Date: 12/12/21 19:05
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List
import airquality.database.exe.abc as exetype
import airquality.database.repo.geolocation as dbrepo
import airquality.api.resp.abc as resptype
import airquality.types.timestamp as tstype


# ------------------------------- GeolocationQueryExecutor ------------------------------- #
class GeolocationQueryExecutor(exetype.QueryExecutorABC):

    def __init__(self, db_repo: dbrepo.SensorGeoRepo):
        self.db_repo = db_repo

    ################################ execute() ###############################
    def execute(self, data: List[resptype.InfoAPIRespTypeABC]) -> None:
        now = tstype.CurrentTimestamp()
        name2id = self.db_repo.name2id

        query2 = self.db_repo.geolocation_query
        query1 = ""
        for resp in data:
            sensor_id = name2id[resp.sensor_name()]
            query1 += self.db_repo.update_location_valid_to_timestamp.format(ts=now.ts, sens_id=sensor_id)
            query2 += self._geo2sql(sensor_id=sensor_id, valid_from=now.ts, response=resp)

        query2exec = f"{query1}; {query2.strip(',')};"
        self.db_repo.push(query2exec)

    ################################ _geo2sql() ###############################
    def _geo2sql(self, sensor_id: int, valid_from: str, response: resptype.InfoAPIRespTypeABC) -> str:
        geom = response.geolocation().geom_from_text()
        return f"({sensor_id}, '{valid_from}', {geom}),"
