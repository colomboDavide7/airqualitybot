######################################################
#
# Author: Davide Colombo
# Date: 06/12/21 20:34
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List, Dict, Tuple
import airquality.database.repo.repo as baserepo
import airquality.types.lookup.lookup as lookuptype
import airquality.database.conn.adapt as dbadapt
import airquality.database.util.query as qry
import airquality.types.postgis as pgistype
import airquality.types.apiresp.inforesp as resptype


class SensorGeoRepository(baserepo.DatabaseRepoABC):

    def __init__(self, db_adapter: dbadapt.DatabaseAdapter, query_builder: qry.QueryBuilder, sensor_type: str, postgis_cls=pgistype.PostgisPoint):
        super(SensorGeoRepository, self).__init__(db_adapter=db_adapter, query_builder=query_builder)
        self.sensor_type = sensor_type
        self.postgis_cls = postgis_cls

    @property
    def name2id(self) -> Dict[str, int]:
        query2exec = self.query_builder.select_sensor_id_name_from_type(self.sensor_type)
        db_lookup = self.db_adapter.send(query2exec)
        return {sensor_name: sensor_id for sensor_id, sensor_name in db_lookup}

    @property
    def database_locations(self) -> Dict[str, str]:
        return {single_lookup.sensor_name: single_lookup.geometry.as_text() for single_lookup in self.lookup()}

    ################################ lookup() ################################
    def lookup(self) -> List[lookuptype.SensorGeoLookup]:
        query2exec = self.query_builder.select_sensor_id_name_from_type(self.sensor_type)
        db_lookup = self.db_adapter.send(query2exec)
        return [lookuptype.SensorGeoLookup(sensor_name=sensor_name, geometry=self.geometry_lookup(sensor_id))
                for sensor_id, sensor_name in db_lookup]

    def geometry_lookup(self, sensor_id: int) -> pgistype.PostgisGeometry:
        query2exec = self.query_builder.select_location_from_sensor_id(sensor_id)
        db_lookup = self.db_adapter.send(query2exec)
        return self.postgis_cls(lat=db_lookup[0][1], lng=db_lookup[0][0])

    ################################ push() ################################
    def push(self, responses: List[resptype.SensorInfoResponse]) -> None:
        if not responses:
            return

        update_query, geolocation_values = self.responses2sql(responses)
        geolocation_query = self.query_builder.build_insert_sensor_location_query(geolocation_values)
        query2exec = update_query + geolocation_query
        self.db_adapter.send(query2exec)

    ################################ responses2sql() ################################
    def responses2sql(self, responses: List[resptype.SensorInfoResponse]) -> Tuple[str, str]:
        update_query = ""
        geolocation_values = ""
        for r in responses:
            update_query += self.query_builder.build_update_location_validity_query(
                valid_to=r.geolocation.timestamp.ts, sensor_id=self.name2id[r.sensor_name]
            )
            geolocation_values += r.geo2sql(self.name2id[r.sensor_name])
        return update_query, geolocation_values.strip(',')
