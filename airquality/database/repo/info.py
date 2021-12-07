######################################################
#
# Author: Davide Colombo
# Date: 06/12/21 19:08
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import itertools
from typing import List
import airquality.database.repo.repo as baserepo
import airquality.types.lookup.lookup as lookuptype
import airquality.database.conn.adapt as adapt
import airquality.database.util.query as qry
import airquality.types.apiresp.inforesp as resp


class SensorInfoRepository(baserepo.DatabaseRepoABC):

    def __init__(self, db_adapter: adapt.DatabaseAdapter, query_builder: qry.QueryBuilder, sensor_type: str):
        super(SensorInfoRepository, self).__init__(db_adapter=db_adapter, query_builder=query_builder)
        self.sensor_type = sensor_type

    def lookup(self) -> List[lookuptype.SensorInfoLookup]:
        query2exec = self.query_builder.select_sensor_id_name_from_type(self.sensor_type)
        db_lookup = self.db_adapter.send(query2exec)
        return [lookuptype.SensorInfoLookup(sensor_name=sensor_name) for sensor_id, sensor_name in db_lookup]

    def lookup_names(self) -> List[str]:
        return [r.sensor_name for r in self.lookup()]

    def push(self, responses: List[resp.SensorInfoResponse]) -> None:

        sensor_values = ""
        apiparam_values = ""
        geolocation_values = ""

        start_id = self.get_max_sensor_id()
        sensor_id_iter = itertools.count(start_id)
        for response in responses:
            sensor_id = next(sensor_id_iter)
            sensor_values += response.sensor2sql(sensor_id)
            apiparam_values += response.apiparam2sql(sensor_id)
            geolocation_values += response.geo2sql(sensor_id)

        query2exec = self.query_builder.build_initialize_sensor_query(
            sensor_values=sensor_values.strip(','),
            api_param_values=apiparam_values.strip(','),
            geolocation_values=geolocation_values.strip(',')
        )
        self.db_adapter.send(query2exec)

    def get_max_sensor_id(self):
        query2exec = self.query_builder.select_max_sensor_id()
        db_lookup = self.db_adapter.send(query2exec)
        max_id = db_lookup[0][0]
        return 1 if max_id is None else (max_id + 1)
