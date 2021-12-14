######################################################
#
# Author: Davide Colombo
# Date: 14/12/21 09:46
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import itertools
from typing import List
import airquality.database.sql.abc as sqlabc
import airquality.file.json as filetype
import airquality.api.resp.abc as resptype
import airquality.types.timestamp as tstype


# ------------------------------- InfoSQLBuilder ------------------------------- #
class InfoSQLBuilder(sqlabc.SQLBuilderABC):

    def __init__(self, start_id: int, sql_queries: filetype.JSONFile):
        self.start_id = start_id
        self.sql_file = sql_queries

    ################################ sql() ###############################
    def sql(self, data: List[resptype.InfoAPIRespTypeABC]) -> str:
        sensor_values = self.sql_file.i3
        apiparam_values = self.sql_file.i4
        geolocation_values = self.sql_file.i5

        sensor_id_iter = itertools.count(self.start_id)
        for resp in data:
            sensor_id = next(sensor_id_iter)
            sensor_values += self._sensor2sql(sensor_id=sensor_id, response=resp)
            apiparam_values += self._apiparam2sql(sensor_id=sensor_id, response=resp)
            geolocation_values += self._geo2sql(sensor_id=sensor_id, response=resp)

        return f"{sensor_values.strip(',')}; {apiparam_values.strip(',')}; {geolocation_values.strip(',')};"

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
