######################################################
#
# Author: Davide Colombo
# Date: 06/12/21 20:34
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List, Dict
import airquality.database.repo.abc as repoabc
import airquality.database.adapt as dbadapt
import airquality.file.json as filetype
import airquality.types.postgis as pgistype


# ------------------------------- GeoLookupType ------------------------------- #
class GeoLookupType(object):

    def __init__(self, sensor_name: str, geometry: pgistype.PostgisGeometry):
        self.sensor_name = sensor_name
        self.geometry = geometry


# ------------------------------- SensorGeoRepo ------------------------------- #
class SensorGeoRepo(repoabc.DatabaseRepoABC):

    def __init__(self, db_adapter: dbadapt.DBAdaptABC, sql_queries: filetype.JSONFile, sensor_type: str, postgis_cls=pgistype.PostgisPoint):
        super(SensorGeoRepo, self).__init__(db_adapter=db_adapter, sql_queries=sql_queries)
        self.sensor_type = sensor_type
        self.postgis_cls = postgis_cls

    @property
    def name2id(self) -> Dict[str, int]:
        query2exec = self.sql_queries.s3.format(personality=self.sensor_type)
        db_lookup = self.db_adapter.execute(query2exec)
        return {sensor_name: sensor_id for sensor_id, sensor_name in db_lookup}

    @property
    def database_locations(self) -> Dict[str, str]:
        return {single_lookup.sensor_name: single_lookup.geometry.as_text() for single_lookup in self.lookup()}

    @property
    def geolocation_query(self) -> str:
        return self.sql_queries.i5

    @property
    def update_location_valid_to_timestamp(self) -> str:
        return self.sql_queries.u1

    ################################ lookup() ################################
    def lookup(self) -> List[GeoLookupType]:
        query2exec = self.sql_queries.s3.format(personality=self.sensor_type)
        db_lookup = self.db_adapter.execute(query2exec)
        return [GeoLookupType(sensor_name=sensor_name, geometry=self._geometry_lookup(sensor_id)) for sensor_id, sensor_name in db_lookup]

    ################################ _geometry_lookup() ################################
    def _geometry_lookup(self, sensor_id: int) -> pgistype.PostgisGeometry:
        query2exec = self.sql_queries.s6.format(sensor_id=sensor_id)
        db_lookup = self.db_adapter.execute(query2exec)
        return self.postgis_cls(lat=db_lookup[0][1], lng=db_lookup[0][0])
