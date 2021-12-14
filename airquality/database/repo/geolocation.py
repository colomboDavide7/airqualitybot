######################################################
#
# Author: Davide Colombo
# Date: 14/12/21 10:41
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List, Dict
import airquality.database.repo.abc as sqlabc
import airquality.file.json as filetype
import airquality.database.conn as dbtype
import airquality.api.resp.abc as resptype
import airquality.types.timestamp as tstype


# ------------------------------- GeolocationDBRepo ------------------------------- #
class GeolocationDBRepo(sqlabc.DBRepoABC):

    def __init__(self, sensor_name2id: Dict[str, int], db_adapter: dbtype.DBConnABC, sql_queries: filetype.JSONFile):
        self.sensor_name2id = sensor_name2id
        self.sql_queries = sql_queries
        self.db_adapter = db_adapter

    ################################ push() ###############################
    def push(self, data: List[resptype.InfoAPIRespTypeABC]) -> None:
        now = tstype.CurrentTimestamp()
        query2 = self.sql_queries.i5
        query1 = ""
        for resp in data:
            sensor_id = self.sensor_name2id[resp.sensor_name()]
            query1 += self.sql_queries.u1.format(ts=now.ts, sens_id=sensor_id)
            query2 += self._geo2sql(sensor_id=sensor_id, timestamp=now, response=resp)

        query2exec = f"{query1}; {query2.strip(',')};"
        self.db_adapter.execute(query2exec)

    ################################ _geo2sql() ###############################
    def _geo2sql(self, sensor_id: int, timestamp: tstype.Timestamp, response: resptype.InfoAPIRespTypeABC) -> str:
        valid_from = timestamp.ts
        geom = response.geolocation().geom_from_text()
        return f"({sensor_id}, '{valid_from}', {geom}),"
