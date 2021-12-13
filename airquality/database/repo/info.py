######################################################
#
# Author: Davide Colombo
# Date: 06/12/21 19:08
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List
import airquality.database.repo.abc as baserepo
import airquality.database.conn.adapt as dbadapt
import airquality.file.json as filetype


# ------------------------------- InfoLookupType ------------------------------- #
class InfoLookupType(object):

    def __init__(self, sensor_name: str):
        self.sensor_name = sensor_name


# ------------------------------- SensorInfoRepository ------------------------------- #
class SensorInfoRepo(baserepo.DatabaseRepoABC):

    def __init__(self, db_adapter: dbadapt.DatabaseAdapter, sql_queries: filetype.JSONFile, sensor_type: str):
        super(SensorInfoRepo, self).__init__(db_adapter=db_adapter, sql_queries=sql_queries)
        self._sensor_type = sensor_type

    @property
    def database_sensor_names(self) -> List[str]:
        return [lookup.sensor_name for lookup in self.lookup()]

    @property
    def max_sensor_id(self) -> int:
        query2exec = self.sql_queries.s1
        db_lookup = self.db_adapter.send(query2exec)
        max_id = db_lookup[0][0]
        return 1 if max_id is None else (max_id + 1)

    @property
    def sensor_query(self) -> str:
        return self.sql_queries.i3

    @property
    def apiparam_query(self) -> str:
        return self.sql_queries.i4

    @property
    def geolocation_query(self) -> str:
        return self.sql_queries.i5

    ################################ lookup() ###############################
    def lookup(self) -> List[InfoLookupType]:
        query2exec = self.sql_queries.s3.format(personality=self._sensor_type)
        db_lookup = self.db_adapter.send(query2exec)
        return [InfoLookupType(sensor_name=sensor_name) for sensor_id, sensor_name in db_lookup]
