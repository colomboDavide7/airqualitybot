######################################################
#
# Author: Davide Colombo
# Date: 06/12/21 20:34
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List, Dict
import airquality.database.repo.repo as baserepo
import airquality.types.lookup.lookup as lookuptype
import airquality.database.conn.adapt as adapt
import airquality.database.util.query as qry
import airquality.types.postgis as pgistype
import airquality.types.apiresp.inforesp as resp


class SensorGeoRepository(baserepo.DatabaseRepoABC):

    def __init__(self, db_adapter: adapt.DatabaseAdapter, query_builder: qry.QueryBuilder, sensor_type: str, postgis_cls=pgistype.PostgisPoint):
        super(SensorGeoRepository, self).__init__(db_adapter=db_adapter, query_builder=query_builder)
        self.sensor_type = sensor_type
        self.postgis_cls = postgis_cls

    def lookup(self) -> List[lookuptype.SensorGeoLookup]:
        query2exec = self.query_builder.select_sensor_id_name_from_type(self.sensor_type)
        db_lookup = self.db_adapter.send(query2exec)
        return [lookuptype.SensorGeoLookup(sensor_name=sensor_name, geometry=self.geometry_lookup(sensor_id))
                for sensor_id, sensor_name in db_lookup]

    def geometry_lookup(self, sensor_id: int) -> pgistype.PostgisGeometry:
        query2exec = self.query_builder.select_location_from_sensor_id(sensor_id)
        db_lookup = self.db_adapter.send(query2exec)
        return self.postgis_cls(lat=db_lookup[0][1], lng=db_lookup[0][0])

    def lookup_locations(self) -> Dict[str, str]:
        return {single_lookup.sensor_name: single_lookup.geometry.as_text() for single_lookup in self.lookup()}

    def push(self, responses: List[resp.SensorInfoResponse]) -> None:
        name2id = self.get_sensor_name2id()

        update_query = ''.join(
            self.query_builder.build_update_location_validity_query(
                valid_to=r.geolocation.timestamp.get_formatted_timestamp(),
                sensor_id=name2id[r.sensor_name]
            ) for r in responses)

        geolocation_values = "".join(r.geo2sql(name2id[r.sensor_name]) for r in responses).strip(',')
        geolocation_query = self.query_builder.build_insert_sensor_location_query(geolocation_values=geolocation_values)
        query2exec = update_query + geolocation_query
        self.db_adapter.send(query2exec)

    def get_sensor_name2id(self) -> Dict[str, int]:
        query2exec = self.query_builder.select_sensor_id_name_from_type(self.sensor_type)
        db_lookup = self.db_adapter.send(query2exec)
        return {sensor_name: sensor_id for sensor_id, sensor_name in db_lookup}
